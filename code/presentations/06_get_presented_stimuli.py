import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

input_dir = "/storage2/wp7/allendata"
session_id = 715093703

manifest_path = os.path.join(input_dir, "manifest.json")
cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)
pres = pd.read_csv("data/presentations/01_presentations_original.csv")
pres = pres[pres["session_id"] == session_id]

scene_frames = np.sort(
    pres.loc[pres["stimulus_name"] == "natural_scenes", "frame"]
    .dropna()
    .astype(int)
    .unique()
)
# Keep only non-negative frames, negative frame is a missing stimulus presentation
scene_frames = scene_frames[scene_frames >= 0]

movie_one_frames = np.sort(
    pres.loc[pres["stimulus_name"] == "natural_movie_one", "frame"]
    .dropna()
    .astype(int)
    .unique()
)
movie_one_frames = movie_one_frames[movie_one_frames >= 0]

movie_three_frames = np.sort(
    pres.loc[pres["stimulus_name"] == "natural_movie_three", "frame"]
    .dropna()
    .astype(int)
    .unique()
)
movie_three_frames = movie_three_frames[movie_three_frames >= 0]

output_dir = Path("data/presentations/presented_stimuli")
scene_dir = output_dir / "natural_scenes"
movie_one_dir = output_dir / "natural_movie_one"
movie_three_dir = output_dir / "natural_movie_three"
scene_dir.mkdir(parents=True, exist_ok=True)
movie_one_dir.mkdir(parents=True, exist_ok=True)
movie_three_dir.mkdir(parents=True, exist_ok=True)

print("Start saving stimulus frames...")

for frame in scene_frames:
    img = cache.get_natural_scene_template(int(frame))
    plt.imsave(scene_dir / f"{frame}.png", img, cmap="gray", vmin=0, vmax=255)

print("Finished saving natural scenes. Now saving natural movie one...")

movie = cache.get_natural_movie_template(1)
for frame in movie_one_frames:
    plt.imsave(movie_one_dir / f"{frame}.png", movie[frame], cmap="gray", vmin=0, vmax=255)

print("Finished saving natural movie one. Now saving natural movie three...")

movie = cache.get_natural_movie_template(3)
for frame in movie_three_frames:
    plt.imsave(
        movie_three_dir / f"{frame}.png", movie[frame], cmap="gray", vmin=0, vmax=255
    )

print("Finished saving all stimulus frames.")
