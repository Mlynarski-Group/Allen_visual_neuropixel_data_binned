from pathlib import Path

import xarray as xr

stim_types = ["natural_movie_one", "natural_movie_three", "natural_scenes"]

in_dir = Path("data/02_stimulus_types")
out_dir = Path("data/03_subset_natural_visual")
out_dir.mkdir(parents=True, exist_ok=True)

for stim in stim_types:
    in_path = in_dir / f"{stim}.h5"
    out_path = out_dir / f"{stim}.h5"

    dt = xr.open_datatree(in_path)
    subset = xr.DataTree()

    for session_name, session_node in dt.children.items():
        sess_subset = xr.DataTree(name=session_name)
        for structure_name, structure_node in session_node.children.items():
            if structure_name.startswith("VIS"):
                sess_subset[structure_name] = structure_node.copy()
        if sess_subset.children:
            subset[session_name] = sess_subset

    subset.to_netcdf(out_path, engine="h5netcdf")
