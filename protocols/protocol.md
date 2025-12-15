# Target format
(Meeting with Augustine 05.12.2025)
- One h5 file per stimulus type
- Within each h5 file, different 3D tensors for each brain area and each session
- 3D tensor shape: neurons x time x trials
- Spiking data in binary format for 20 ms bins

# cmd commands
## Installation
```bash
conda create -n allensdk python=3.9 pip
pip install allensdk
pip install ipykernel
```
## Running the code
```bash
nohup ./code/datalad_wrapper.sh & echo $! > logs/run.pid  # Start remote job with wrapper
ps -p $(cat logs/run.pid)  # Check if job is running
tail -n 200 logs/run.log  # Print log to terminal
```

Running speed time resolution:  0.01533 / 0.03304 seconds

Along dimensions time/trials: speed, pupil data
Along dimensions neurons: brain area, unit_analysis_metrics (for each stimulus type)?
Along dimensions trials: stimulus condition (e.g. orientation, spatial frequency, contrast, etc)

# Session attributes
- session type

# Relevant stimulus parameters
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

# Assembling data
- natural_movie_one_more_repeats and natural_movie_one

# Filtered out stimulus types
- spontaneous
- shuffled movies
- 'invalid_presentation'

# Filtered out stimulus presentations
- **-1 frame values in natural scenes**: no stimulus shown
- **'null' values in gratings of brain_observatory_1.1**: in brain_observatory_1.1 sessions,
    some *drifting_gratings* and *static_gratings* stimulus presentations have 'null' values.
    Blank trials with no stimulus presented.
