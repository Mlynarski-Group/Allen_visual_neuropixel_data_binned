"""Utilities to export per-session arrays from stimulus `.h5` files.

Usage as a Python module
------------------------
Import and call `access_stimulus_structure`:

    from code.utils.access_stimulus_structure import access_stimulus_structure
    access_stimulus_structure("natural_movie_one", "VISp", "data/out")

Arguments:
- `stimulus` (str): stimulus type to access (e.g., 'natural_movie_one').
- `structure` (str): brain structure key inside each session tree.
- `out_path` (str | Path): output directory where `.npy` files are written.
- `data` (str, optional): one of `"spike_data"` or `"speed"`. Default: `"spike_data"`.

Usage from command line
-----------------------
Run the file in the dataset root directory with the following command:

    python code/utils/access_stimulus_structure.py \
        <stimulus> <structure> <out_path> [--data {spike_data,speed}]

CLI arguments:
- `stimulus`: same as module argument.
- `structure`: same as module argument.
- `out_path`: same as module argument.
- `--data`: same as module argument; defaults to `spike_data`.
"""

import argparse
from pathlib import Path

import numpy as np
import xarray as xr

# IN_PATH = Path("data/02_stimulus_types")
IN_PATH = Path("data/03_subset_natural_visual")

def access_stimulus_structure(stimulus, structure, out_path, data='spike_data'):
    """Access .h5 files by stimulus type and structure and save as .npy files.

    In out_path saves per-session .npy files in the format:
    session_{session_id}-{stimulus}-{structure}-{data}.npy

    Dimensions of saved arrays:
    - Spikes: neurons x presentations x time
    - Speed: presentations x time
    
    Parameters
    ----------
    stimulus : str
        Stimulus type to access (e.g., 'natural_movie_one').
    structure : str
        Brain structure key to access in each session (e.g., 'VISp').
    out_path : str or Path
        Output directory where per-session `.npy` files are saved.
    data : str, optional
        Data key to extract from each structure: 'spike_data' or 'speed'.
        Default is 'spike_data'.
    """
    if data not in ["spike_data", "speed"]:
        raise ValueError("data must be one of 'spike_data' or 'speed'")

    stim_path = IN_PATH / f"{stimulus}.h5"
    if not stim_path.exists():
        raise FileNotFoundError(f"Stimulus data not found for stimulus {stimulus}")

    out_path = Path(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    print("Opening data tree for stimulus:", stimulus)
    dt = xr.open_datatree(stim_path, engine="h5netcdf")
    n_sessions = 0

    print("Tree opened")

    for session_name, session_node in dt.children.items():
        if structure not in session_node.children:
            continue
        struct_node = session_node[structure]
        if data not in struct_node.children:
            continue
        data_node = struct_node[data]
        ds = data_node.ds
        xr_obj = ds[data]

        if data == "spike_data":
            xr_obj = xr_obj.transpose("unit_id", "presentation_id", "time")
        else:
            xr_obj = xr_obj.transpose("presentation_id", "time")

        arr = xr_obj.to_numpy()
        out_file = out_path / f"{session_name}-{stimulus}-{structure}-{data}.npy"
        np.save(out_file, arr)
        n_sessions += 1

    dt.close()

    print(f"{n_sessions} sessions extracted for stimulus {stimulus} and structure {structure}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Extract per-session arrays for a stimulus and structure."
    )
    parser.add_argument("stimulus", help="Stimulus type, e.g. natural_movie_one")
    parser.add_argument("structure", help="Brain structure, e.g. VISp")
    parser.add_argument("out_path", help="Output directory for .npy files")
    parser.add_argument(
        "--data",
        default="spike_data",
        choices=["spike_data", "speed"],
        help="Data type to extract",
    )
    args = parser.parse_args()

    access_stimulus_structure(args.stimulus, args.structure, args.out_path, args.data)
