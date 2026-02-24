# Target format
- One h5 file per stimulus type
- Within each h5 file, different 3D tensors for each brain area and each session
- 3D tensor shape: neurons x time x trials
- Spiking data in binary format for 20 ms bins

# Output files' structure
```
/ {stimulus_type}.h5
    / session_{session_id}
        / {brain_structure}
            / spike_data: xarray.DataArray (presentation_id x unit_id x time)
            / speed: xarray.DataArray (presentation_id x time)
            / pupil_data: xarray.DataSet (presentation_id x time): pupil_variables
            / presentations: xarray.DataSet (presentation_id):
                ['stimulus_block', 'start_time', 'stop_time', 'duration']
                + relevant_stimulus_parameters
```

## Relevant stimulus parameters
```
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
```

## Data dimensions
- Along dimension time: spike_data, speed, pupil_data
- Along dimension neurons: spike_data
- Along dimension trials: spike_data, speed, pupil_data, presentations

# Data
## Main data files
- [data/02_stimulus_types/](data/02_stimulus_types/): h5 files per stimulus type with processed data tensors
- [data/03_subset_natural_visual](data/03_subset_natural_visual/): subset of h5 files for natural stimuli (natural_movie_one, natural_movie_three, natural_scenes) with only visual cortex areas
- [data/presentations/03_presentations_filtered_by_duration.csv](data/presentations/03_presentations_filtered_by_duration.csv): All presentations remaining after filtering out presentations with irregular durations
- [data/combined_statistics.csv](data/combined_statistics.csv): Summary statistics of the numbers of units and presentations per stimulus type, session, and brain structure

## Additional data files
- [data/sessions.csv](data/sessions.csv): Summary of all sessions (allen sdk metadata)
- [data/units.csv](data/units.csv): Summary of all units (allen sdk metadata)
- [docs/All_presentation_parameters.csv](docs/All_presentation_parameters.csv): All unique stimulus parameters for all stimulus types and all presentations
- [docs/presentations_median_durations.csv](docs/presentations_median_durations.csv): Actual median durations used for filtering presentations per stimulus type
- [docs/presentations_filtered_summary.csv](docs/presentations_filtered_summary.csv): Summary of number of presentations before and after filtering per stimulus type

## Data size
- data/01_sessions_presentations/: 11.99 GB
- data/02_stimulus_types/: 18.82 GB
- data/03_subset_natural_visual/: 3.19 GB
- data/presentations/: 827.55 MB
- data/combined_statistics.csv: 250.69 KB
- data/sessions.csv: 13.19 KB
- data/units.csv: 21.65 MB

# Actions taken on data
## Combined stimulus types
- natural_movie_one_more_repeats and natural_movie_one
## **Not** combined stimulus types
- drifting_gratings and drifting_gratings_75_repeats,  
    because they have different set of stimulus parameters 
    (brain_observatory_1.1 vs functional_connectivity)
- drifting_gratings_contrast and drifting_gratings_75_repeats (functional_connectivity),  
     because they have different duration

## Filtered out stimulus types
- spontaneous
- shuffled movies
- 'invalid_presentation'

## Filtered out stimulus presentations
- **-1 frame values in natural scenes**: no stimulus shown
- **'null' values in gratings and dot_motion**: some stimulus presentations have 'null' values in:
    - drifting_gratings
    - static_gratings
    - dot_motion
    Those are blank trials with no stimulus presented.
- **Presentations with irregular durations**:
    - For each stimulus type, compute the median duration of all presentations
    - Filter out presentations with durations deviating from the median by more than:
        - 0.01 s for natural movies
        - 0.001 s for other types

### Summary of filtered presentations
gabors: 211361 - 211282 = 79 (0.04%)  
flashes: 8696 - 8694 = 2 (0.02%)  
drifting_gratings: 20146 - 20129 = 17 (0.08%)  
natural_movie_three: 320 - 314 = 6 (1.88%)  
natural_movie_one: 640 - 628 = 12 (1.88%)  
static_gratings: 191360 - 191336 = 24 (0.01%)  
natural_scenes: 190362 - 190323 = 39 (0.02%)  
drifting_gratings_contrast: 18360 - 18355 = 5 (0.03%)  
natural_movie_one_more_repeats: 1559 - 1551 = 8 (0.51%)  
drifting_gratings_75_repeats: 15600 - 15591 = 9 (0.06%)  
dot_motion: 11070 - 11031 = 39 (0.35%)  
[docs/presentations_filtered_summary.csv](docs/presentations_filtered_summary.csv)  

### Actual median durations used for filtering
gabors: 0.2502 s  
flashes: 0.2502 s  
drifting_gratings: 2.0017 s  
natural_movie_three: 120.1003 s  
natural_movie_one: 30.0251 s  
static_gratings: 0.2502 s  
natural_scenes: 0.2502 s  
drifting_gratings_contrast: 0.5004 s  
natural_movie_one_more_repeats: 30.0251 s  
drifting_gratings_75_repeats: 2.0017 s  
dot_motion: 1.0008 s  
[docs/presentations_median_durations.csv](docs/presentations_median_durations.csv)

## Applied data processing
- Bin and binarize spiking data into 20 ms bins, including *longest* stimulus presentations
- Only count spikes within each presentation's duration (for movies)
- Align times to stimulus onset
- Label bins by center time
- Align running speed to spiking bins by linear interpolation
- Align all pupil data variables to spiking bins by linear interpolation  

# Notebook
[Notebook](presentation/Data_exploration_notebook.ipynb) contains code for accessing row Allen SDK data and exploring the processed data.  
Loading allen sdk data requires [allensdk-env](envs/allensdk_env.yml) conda environment.  
Loading processed data requires [xarray-env](envs/xarray_env.yml) conda environment.  
(See [Environments](#environments) section below)

# Plots
- [Units per brain structure, stacked by stimulus type](figures/units_per_structure_by_stimulus_stacked.png)
- [Units per brain structure, grouped by stimulus type](figures/units_per_structure_by_stimulus_multibar.png)
- [Units per session, stacked by brain structure](figures/units_per_session_by_structure.png)
- [Units per session, stacked by brain structure, faceted by stimulus type](figures/units_per_session_by_structure_stimulus.png)
- [Presentations per brain structure, stacked by stimulus type](figures/presentations_per_structure_by_stimulus_stacked.png)
- [Presentations per brain structure, grouped by stimulus type](figures/presentations_per_structure_by_stimulus_multibar.png)
- [Presentations per session, stacked by structure, faceted by stimulus type](figures/presentations_per_session_by_structure_stimulus.png)
- [Sessions per stimulus type, stacked by session type](figures/sessions_per_stimulus.png)
- [Example spike raster bins for one presentation](figures/example_spikes_over_bins.png)

# Scripts
## access_stimulus_structure.py
    - Access .h5 files by stimulus type, brain structure, data type (spikes or speed)
    - Save to given output path as .npy files, one per session
    - Dimensions of saved arrays:
        - Spikes: neurons x presentations x time
        - Speed: presentations x time

### Usage as Python module
```python
from code.utils.access_stimulus_structure import access_stimulus_structure

access_stimulus_structure(
    stimulus,           # stimulus type to access
    structure,          # brain structure
    out_path,           # output directory for per-session .npy files
    data="spike_data",  # "spike_data" (default) or "speed"
)
```
Example:
```python
access_stimulus_structure(
    stimulus="natural_movie_one",
    structure="VISp",
    out_path="data/npy_out",
    data="spike_data",
)
```

### Usage as command line script
```bash
python code/utils/access_stimulus_structure.py \
    <stimulus> <structure> <out_path> [--data {spike_data,speed}]
```
Example:
```bash
python code/utils/access_stimulus_structure.py natural_movie_one VISp data/npy_out --data spike_data
```

# cmd commands
## Data download
```bash
datalad clone https://github.com/Mlynarski-Group/Allen_visual_neuropixel_data_binned
OR
git clone https://github.com/Mlynarski-Group/Allen_visual_neuropixel_data_binned

cd Allen_visual_neuropixel_data_binned

datalad get /path/to/file/or/directory
OR
git annex get /path/to/file/or/directory
```

## Environments
Allensdk requires python 3.9, but xarray requires latest versions (xarray > v2025.10.0) to work with DataTrees.
```bash
conda env create -f envs/allensdk_env.yml
conda env create -f envs/xarray_env.yml
```

## New allensdk installation
```bash
conda create -n allensdk python=3.9 pip
pip install allensdk
pip install ipykernel
```

## Running heavy code for dataset creation
```bash
nohup setsid ./code/datalad_wrapper.sh & echo $! > logs/run.pid  # Start remote job with wrapper
ps -p $(cat logs/run.pid)  # Check if job is running
```
