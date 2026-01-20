import gc
import logging
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

# tell pandas to show all columns when we display a DataFrame
pd.set_option("display.max_columns", None)

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("logs/run.log")])
log = logging.getLogger()

# Quiet noisy allensdk logger
lg = logging.getLogger("call_caching")
for h in lg.handlers[:]:
    lg.removeHandler(h)
lg.setLevel(logging.WARNING)

relevant_stimulus_parameters = {
    'gabors': ['orientation', 'y_position', 'x_position'],
    'flashes': ['color'],
    'drifting_gratings': ['temporal_frequency', 'orientation'],
    'static_gratings': ['phase', 'spatial_frequency', 'orientation'],
    'natural_scenes': ['frame'],
    'natural_movie_one': ['frame'],
    'natural_movie_three': ['frame'],
    'natural_movie_one_more_repeats': ['frame'],
    'drifting_gratings_contrast': ['contrast', 'orientation'],
    'drifting_gratings_75_repeats': ['contrast', 'orientation'],
    'dot_motion': ['Speed', 'Dir']
}

invalid_stimulus_substr = ['spontaneous', 'shuffled', 'invalid']
filtered_presentations_path = Path(
    "data/presentations/03_presentations_filtered_by_duration.csv"
)

completed_sessions_path = Path("logs/completed_sessions")
completed_sessions = []
if completed_sessions_path.exists():
    with completed_sessions_path.open() as f:
        completed_sessions = [int(l.strip()) for l in f if l.strip()]


def process_session(cache, session_id, presentations_by_session):
    session = cache.get_session_data(session_id)
    log.info("Session %s loaded.", session_id)

    session_presentations = presentations_by_session[session_id]

    stimulus_types = session_presentations['stimulus_name'].unique().tolist()
    stimulus_types = [st for st in stimulus_types
                      if all(substr not in st for substr in invalid_stimulus_substr)]

    running_speed = session.running_speed
    gaze_data = session.get_screen_gaze_data()
    log.info('Obtained running speed and gaze data.')
    unit_ids = session.units.index.values

    output_folder = Path(f'logs/data/01_sessions_presentations/session_{session_id}/')
    output_folder.mkdir(parents=True, exist_ok=True)

    for stimulus_type in stimulus_types:
        log.info("\tProcessing stimulus type: %s", stimulus_type)
        process_stimulus_type(
            stimulus_type,
            session,
            unit_ids,
            session_presentations,
            output_folder,
            running_speed,
            gaze_data,
        )

    # Free memory
    del session
    gc.collect()

def process_stimulus_type(stimulus_type, session, unit_ids, session_presentations,
                          output_folder, running_speed, gaze_data):
    type_presentations = get_type_presentations(
        stimulus_type, session_presentations)
    if type_presentations.empty:
        log.warning("\t\tNo presentations of type %s.", stimulus_type)
        return

    # Compute spike counts
    is_natural_movie = 'natural_movie' in stimulus_type
    spike_counts = compute_spike_counts(
        type_presentations, session, unit_ids, apply_clip=is_natural_movie)
    # Get running speed and gaze data aligned to presentations
    type_running_speed = get_running_speed(
        spike_counts, running_speed, type_presentations)
    if gaze_data is not None:
        type_gaze_data = get_gaze_data(
            spike_counts, gaze_data, type_presentations)
    else:
        type_gaze_data = None

    stimuli = type_presentations.astype(np.float32).to_xarray()

    combine_and_save_data(
        spike_counts,
        type_running_speed,
        type_gaze_data,
        stimuli,
        stimulus_type,
        output_folder
    )

def get_type_presentations(stimulus_type, session_presentations):
    type_presentations = session_presentations[
        session_presentations['stimulus_name'] == stimulus_type
    ]

    # Keep only relevant columns
    params = relevant_stimulus_parameters[stimulus_type]
    stimulus_columns = (params + [
        'stimulus_presentation_id',
        'stimulus_block',
        'start_time',
        'stop_time',
        'duration',
    ])

    type_presentations = type_presentations[stimulus_columns]
    type_presentations = type_presentations.set_index(
        'stimulus_presentation_id', drop=True)

    # Filter out null values for drifting or static gratings
    if 'gratings' in stimulus_type or 'dot_motion' in stimulus_type:
        type_presentations = type_presentations.replace("null", pd.NA)
        type_presentations = type_presentations.dropna()

    # Filter out -1 frame values for natural scenes: these indicate no stimulus shown
    if 'natural_scenes' in stimulus_type:
        type_presentations = type_presentations[type_presentations['frame'] != -1]

    return type_presentations

def compute_spike_counts(presentations, session, unit_ids, bin_width=0.02,
                         apply_clip=True):

    # Create bins including end time
    max_dur = presentations['duration'].max()
    n_bins = int(np.ceil(max_dur / bin_width))
    time_bin_edges = np.arange(0, (n_bins + 1) * bin_width, bin_width)

    # Construct 3D array of binarized spike counts
    ids = presentations.index.values
    kwargs = {
        "bin_edges": time_bin_edges,
        "stimulus_presentation_ids": ids,
        "unit_ids": unit_ids,
        "binarize": True,
    }
    if apply_clip:
        stop_times = presentations['stop_time'].values
        clip_cb = lambda domain: np.minimum(domain, stop_times[:, None])
        kwargs["time_domain_callback"] = clip_cb
    spike_counts = session.presentationwise_spike_counts(**kwargs)

    return spike_counts

def get_running_speed(spike_counts, running_speed, presentations):
    bin_centers = spike_counts.coords["time_relative_to_stimulus_onset"].values
    presentation_ids = spike_counts.coords["stimulus_presentation_id"].values
    running_start_time = running_speed["start_time"]
    running_velocity = running_speed["velocity"]
    out = np.empty((len(bin_centers), len(presentation_ids)), dtype=np.float32)
    for i, pr_id in enumerate(presentation_ids):
        pr_start = presentations.loc[pr_id, "start_time"]
        abs_time = pr_start + bin_centers
        out[:, i] = np.interp(abs_time, running_start_time, running_velocity)
    return xr.DataArray(
        out,
        dims=("time_relative_to_stimulus_onset", "stimulus_presentation_id"),
        coords={
            "time_relative_to_stimulus_onset": bin_centers,
            "stimulus_presentation_id": presentation_ids,
        },
        name="presentationwise_speed",
    )

def get_gaze_data(spike_counts, gaze_data, presentations):
    bin_centers = spike_counts.coords["time_relative_to_stimulus_onset"].values
    presentation_ids = spike_counts.coords["stimulus_presentation_id"].values
    gaze_t = gaze_data.index
    cols = list(gaze_data.columns)
    data_vars = {}
    for col in cols:
        vals = gaze_data[col]
        out = np.empty((len(bin_centers), len(presentation_ids)), dtype=np.float32)
        for i, pr_id in enumerate(presentation_ids):
            pr_start = presentations.loc[pr_id, "start_time"]
            abs_time = pr_start + bin_centers
            out[:, i] = np.interp(abs_time, gaze_t, vals)
        data_vars[col] = (("time_relative_to_stimulus_onset",
                           "stimulus_presentation_id"), out)
    ds = xr.Dataset(
        data_vars,
        coords={
            "time_relative_to_stimulus_onset": bin_centers,
            "stimulus_presentation_id": presentation_ids,
        },
    )
    return ds

def combine_and_save_data(
        spike_counts, running_speed, gaze_data, stimuli, stimulus_type, output_folder):

    spike_counts.to_netcdf(output_folder / f'{stimulus_type}_spike_counts.nc')
    running_speed.to_netcdf(output_folder / f'{stimulus_type}_running_speed.nc')
    if gaze_data is not None:
        gaze_data.to_netcdf(output_folder / f'{stimulus_type}_gaze_data.nc')
    stimuli.to_netcdf(output_folder / f'{stimulus_type}_stimuli.nc')

def main():
    # Define working folder and load the cache
    input_dir = '/storage2/wp7/allendata'
    manifest_path = os.path.join(input_dir, "manifest.json")
    cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)
    log.info("Cache loaded.")

    sessions_table = cache.get_session_table()
    session_ids = sessions_table.index.values.tolist()
    log.info("Found %d sessions.", len(session_ids))

    presentations = pd.read_csv(filtered_presentations_path)
    presentations_by_session = {
        int(session_id): df
        for session_id, df in presentations.groupby('session_id', sort=False)
    }

    # Process each session
    for idx, session_id in enumerate(session_ids, start=1):
        # Skip already completed session
        if session_id in completed_sessions:
            log.info("Skipping already completed session %s.", session_id)
            continue

        log.info("Processing session %s (%d/%d)",
            session_id, idx, len(session_ids))
        t0 = time.perf_counter()
        process_session(cache, session_id, presentations_by_session)
        t1 = time.perf_counter()
        dur = t1 - t0
        log.info("Finished session %s in %.2f seconds.", session_id, dur)

        # Add session to completed
        with completed_sessions_path.open("a") as f:
            f.write(f"{session_id}\n")


if __name__ == '__main__':
    main()
