import gc
import logging
import os
import sys
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
                    handlers=[logging.FileHandler("run.log"),
                              logging.StreamHandler(sys.stdout)])
log = logging.getLogger()

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

completed_sessions = []


def process_session(cache, session_id):
    session = cache.get_session_data(session_id)
    log.info("\nSession %s loaded.", session_id)

    # Access stimulus presentations
    stimulus_types = session.stimulus_names
    # Filter out unwanted stimulus types
    stimulus_types = [st for st in stimulus_types
                      if all(substr not in st for substr in invalid_stimulus_substr)]

    running_speed = session.running_speed
    gaze_data = session.get_screen_gaze_data()
    log.info('Obtained running speed and gaze data.')

    output_folder = Path(f'data/01_sessions_presentations/session_{session_id}/')
    output_folder.mkdir(parents=True, exist_ok=True)

    for stimulus_type in stimulus_types:
        log.info("\tProcessing stimulus type: %s", stimulus_type)
        process_stimulus_type(
            stimulus_type, session, output_folder, running_speed, gaze_data)

    # Free memory
    del session
    gc.collect()

def process_stimulus_type(stimulus_type, session, output_folder,
                          running_speed, gaze_data):
    type_presentations = get_type_presentations(stimulus_type, session)

    # Compute spike counts
    spike_counts = compute_spike_counts(type_presentations, session)
    log.info('\t\tComputed spike counts.')
    # Get running speed and gaze data aligned to presentations
    type_running_speed = get_running_speed(
        spike_counts, running_speed, type_presentations)
    log.info('\t\tComputed running speed.')
    if gaze_data is not None:
        type_gaze_data = get_gaze_data(
            spike_counts, gaze_data, type_presentations)
    else:
        type_gaze_data = None
    log.info('\t\tComputed gaze data.')

    stimuli = type_presentations.astype(np.float32).to_xarray()

    combine_and_save_data(
        spike_counts,
        type_running_speed,
        type_gaze_data,
        stimuli,
        stimulus_type,
        output_folder
    )

def get_type_presentations(stimulus_type, session):
    # Access stimulus presentations of the given type
    type_presentations = session.get_stimulus_table(stimulus_type)

    # Keep only relevant columns
    stimulus_columns = (relevant_stimulus_parameters[stimulus_type] +
                        ['stimulus_block', 'start_time', 'stop_time', 'duration'])
    type_presentations = type_presentations[stimulus_columns]

    # Group movie frame presentations into whole movie presentations
    if 'movie' in stimulus_type:
        type_presentations = whole_movie_presentations(type_presentations)

    # Filter out null values for drifting or static gratings
    if 'gratings' in stimulus_type:
        type_presentations = type_presentations.replace("null", pd.NA)
        type_presentations = type_presentations.dropna()

    return type_presentations

def whole_movie_presentations(presentations):
    df = presentations.reset_index()
    frames = df['frame']
    new_movie = frames.diff().fillna(1) < 0
    df['movie_group'] = new_movie.cumsum()
    agg = df.groupby('movie_group').agg(
        stimulus_block=('stimulus_block', 'first'),
        start_time=('start_time', 'min'),
        stop_time=('stop_time', 'max'),
        first_presentation_id=('stimulus_presentation_id', 'first'),
    )
    agg['duration'] = agg['stop_time'] - agg['start_time']
    agg = agg.set_index('first_presentation_id')
    agg.index.name = 'stimulus_presentation_id'
    return agg

def compute_spike_counts(presentations, session, bin_width = 0.02):

    # Crate bins including end time
    max_dur = presentations['duration'].max()
    n_bins = int(np.ceil(max_dur / bin_width))
    time_bin_edges = np.arange(0, (n_bins + 1) * bin_width, bin_width)

    # Only count spikes up to the stop time of each presentation
    stop_times = presentations['stop_time'].values
    clip_cb = lambda domain: np.minimum(domain, stop_times[:, None])

    # Construct 3D array of binarized spike counts
    ids = presentations.index.values
    unit_ids = session.units.index.values
    spike_counts = session.presentationwise_spike_counts(
        bin_edges=time_bin_edges,
        stimulus_presentation_ids=ids,
        unit_ids=unit_ids,
        binarize=True,
        time_domain_callback=clip_cb
        )

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

    log.info("\t\tFiles for stimulus type %s saved.", stimulus_type)

    # combined_data.to_netcdf(output_folder / f'{stimulus_type}.nc')

def main():
    # Define working folder and load the cache
    input_dir = '/storage2/wp7/allendata'
    manifest_path = os.path.join(input_dir, "manifest.json")
    cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)
    log.info("Cache loaded.")

    # Load sessions_table
    sessions_table = cache.get_session_table()
    session_ids = sessions_table.index.values.tolist()
    log.info("Found %d sessions.", len(session_ids))

    # Process each session
    for session_id in session_ids:
        if session_id in completed_sessions:
            log.info("Skipping already completed session %s.", session_id)
            continue
        log.info("Processing session %s (%d/%d)",
            session_id, session_ids.index(session_id)+1, len(session_ids))
        t0 = time.perf_counter()
        process_session(cache, session_id)
        t1 = time.perf_counter()
        dur = t1 - t0
        log.info("Finished session %s in %.2f seconds.", session_id, dur)


if __name__ == '__main__':
    main()
