# Target format
- One h5 file per stimulus type
- Within each h5 file, different 3D tensors for each brain area and each session
- 3D tensor shape: neurons x time x trials
- Spiking data in binary format for 20 ms bins

# Output files' structure
```
/ {stimulus_type}.h5
    / {brain_structure}
        / session_{session_id}
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

## Applied data processing
- Bin and binarize spiking data into 20 ms bins, including *longest* stimulus presentations
- Only count spikes within each presentation's duration
- Align times to stimulus onset
- Label bins by center time
- ! Align running speed to spiking bins by linear interpolation
- ! Align all pupil data variables to spiking bins by linear interpolation

# cmd commands
## Installation
```bash
conda create -n allensdk python=3.9 pip
pip install allensdk
pip install ipykernel
```
## Running the code
```bash
nohup setsid ./code/datalad_wrapper.sh & echo $! > logs/run.pid  # Start remote job with wrapper
ps -p $(cat logs/run.pid)  # Check if job is running
tail -n 200 logs/run.log  # Print log to terminal
```