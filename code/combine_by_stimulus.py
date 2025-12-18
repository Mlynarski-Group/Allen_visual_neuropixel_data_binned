import logging
import sys
from pathlib import Path

import pandas as pd
import xarray as xr

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stderr),
                              logging.FileHandler("logs/run.log")])
log = logging.getLogger()

def build_all_stimulus_h5(
    units_path="data/units.csv",
    sessions_root="data/01_sessions_presentations",
    out_dir="data/02_stimulus_types",
):
    sessions_root = Path(sessions_root)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    session_ids = discover_session_ids(sessions_root)
    stim_types = discover_all_stim_types(sessions_root, session_ids)

    units = pd.read_csv(units_path, index_col="id")

    for stim_type in stim_types:
        log.info("Processing stimulus type: %s", stim_type)
        write_one_stimulus_file(stim_type, session_ids, units, sessions_root, out_dir)

def discover_session_ids(sessions_root: Path) -> list[int]:
    return sorted(int(p.name.split("_", 1)[1]) for p in sessions_root.glob("session_*"))

def discover_all_stim_types(sessions_root: Path, session_ids: list[int]) -> list[str]:
    stim_names = set()
    for session_id in session_ids:
        session_dir = sessions_root / f"session_{session_id}"
        stim_names |= set(discover_stims_in_session(session_dir))
    return sorted(stim_names)

def discover_stims_in_session(session_dir: Path) -> list[str]:
    suffix = "_spike_counts.nc"
    return sorted(f.name[:-len(suffix)] for f in session_dir.glob(f"*{suffix}"))

def write_one_stimulus_file(
        stim_type: str,
        session_ids: list[int],
        units,
        sessions_root: Path,
        out_dir: Path
    ):
    out_path = out_dir / f"{stim_type}.h5"

    sessions_with_stim = [sid for sid in session_ids
                          if has_stim_type(sessions_root, sid, stim_type)]
    structures = discover_stim_structures(units, sessions_with_stim)

    for structure in structures:
        log.info("  Writing structure: %s", structure)
        write_one_structure_group(
            units, sessions_root, out_path, stim_type, structure, sessions_with_stim)

def has_stim_type(sessions_root: Path, session_id: int, stim_type: str) -> bool:
    session_dir = sessions_root / f"session_{session_id}"
    return (session_dir / f"{stim_type}_spike_counts.nc").exists()

def discover_stim_structures(units, session_ids: list[int]) -> list[str]:
    sess_units = units[units["ecephys_session_id"].isin(session_ids)]
    return sorted(sess_units["ecephys_structure_acronym"].dropna().unique().tolist())

def write_one_structure_group(
    units,
    sessions_root: Path,
    out_path: Path,
    stim: str,
    structure: str,
    session_ids: list[int],
):
    for session_id in session_ids:
        log.info("    Processing session %d", session_id)
        unit_ids = unit_ids_for_session_structure(units, session_id, structure)
        if not unit_ids:
            continue

        session_dir = sessions_root / f"session_{session_id}"
        session_data = load_session_stimulus(session_dir, stim)
        session_data = standardize_names(session_data)
        session_data["spike_data"] = session_data["spike_data"].sel(unit_id=unit_ids)

        write_session_group(out_path, structure, session_id, session_data)

def unit_ids_for_session_structure(units, session_id: int, structure: str) -> list[int]:
    ses_units = units[units["ecephys_session_id"] == session_id]
    ses_struct_units = ses_units[ses_units["ecephys_structure_acronym"] == structure]
    return ses_struct_units.index.to_list()

def load_session_stimulus(session_dir: Path, stim: str) -> dict:
    spikes_da = xr.load_dataarray(session_dir / f"{stim}_spike_counts.nc")
    speed_da = xr.load_dataarray(session_dir / f"{stim}_running_speed.nc")
    presentations_ds = xr.load_dataset(session_dir / f"{stim}_stimuli.nc")

    gaze_path = session_dir / f"{stim}_gaze_data.nc"
    gaze_ds = xr.load_dataset(gaze_path) if gaze_path.exists() else None

    return {
        "spike_counts": spikes_da,
        "running_speed": speed_da,
        "stimuli": presentations_ds,
        "gaze_data": gaze_ds,
    }

def standardize_names(session_data: dict) -> dict:
    spike_data = session_data["spike_counts"].rename(
        {
            "stimulus_presentation_id": "presentation_id",
            "time_relative_to_stimulus_onset": "time",
        }
    ).rename("spike_data")

    speed = session_data["running_speed"].rename(
        {
            "stimulus_presentation_id": "presentation_id",
            "time_relative_to_stimulus_onset": "time",
        }
    ).rename("speed")

    presentations = session_data["stimuli"].rename(
        {"stimulus_presentation_id": "presentation_id"})

    out = {
        "spike_data": spike_data,
        "speed": speed,
        "presentations": presentations,
    }

    gaze_ds = session_data["gaze_data"]
    if gaze_ds is not None:
        out["gaze_data"] = gaze_ds.rename(
            {
                "stimulus_presentation_id": "presentation_id",
                "time_relative_to_stimulus_onset": "time",
            }
        )

    return out

def write_session_group(
        out_path: Path, structure: str, session_id: int, session_data: dict):
    base_group = f"{structure}/session_{session_id}"

    write_xr(session_data["spike_data"], out_path, f"{base_group}/spike_data")
    write_xr(session_data["speed"], out_path, f"{base_group}/speed")
    write_xr(session_data["presentations"], out_path, f"{base_group}/presentations")

    if "gaze_data" in session_data:
        write_xr(session_data["gaze_data"], out_path, f"{base_group}/gaze_data")

def write_xr(xr_obj, out_path: Path, group: str):
    xr_obj.to_netcdf(out_path, engine="h5netcdf",
                     mode="a" if out_path.exists() else "w", group=group)


if __name__ == "__main__":
    build_all_stimulus_h5()
