from pathlib import Path

import matplotlib.image as mpimg
import numpy as np
import xarray as xr

base_dir = Path("data/presentations/presented_stimuli")
stimulus_names = ["natural_scenes", "natural_movie_one", "natural_movie_three"]

for stimulus_name in stimulus_names:
    paths = sorted((base_dir / stimulus_name).glob("*.png"), key=lambda p: int(p.stem))
    frames = np.array([int(path.stem) for path in paths])
    images = []

    for path in paths:
        img = (mpimg.imread(path)[..., 0] * 255).astype(np.uint8)
        images.append(img)

    data = xr.DataArray(
        np.stack(images),
        dims=("frame", "y", "x"),
        coords={"frame": frames},
        name=stimulus_name,
    )
    data.to_netcdf(base_dir / f"{stimulus_name}_frames.h5", engine="h5netcdf")
