# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.20.0
#   kernelspec:
#     display_name: xarray-env
#     language: python
#     name: python3
# ---

# +
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
from allensdk.brain_observatory.ecephys.visualization import (
    raster_plot,
)

# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# tell pandas to show all columns when we display a DataFrame
pd.set_option("display.max_columns", None)
# %config InteractiveShell.ast_node_interactivity = 'all'
# -


# # Load Allen metadata tables

# Define working folder and load the cache
input_dir = '/storage2/wp7/allendata'
manifest_path = os.path.join(input_dir, "manifest.json")
cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)

# +
# Load sessions_table and units_table from the cache
sessions_table = cache.get_session_table()
units_table = cache.get_units()

session_ids = sessions_table.index.values.tolist()
print(f"Found {len(session_ids)} sessions.")

print("Sessions table:")
sessions_table.head()
print("Units table:")
units_table.head()
# -

# # Load a specific session

session_id = 798911424
session = cache.get_session_data(session_id)
print(f"Session {session_id} loaded.")

# # Access stimulus presentations and parameters

# +
# All stimulus presentations
print("All stimulus presentations:")
session.stimulus_presentations.head()

# Stimulus presentations for specific stimulus type
stimulus_type = 'drifting_gratings'
print(f"Stimulus presentations for specific stimulus type ({stimulus_type}):")
session.get_stimulus_table([stimulus_type]).head()
# -

# ## All unique stimulus parameters

# +
# Print unique stimulus parameter values for two types of sessions
print(f"Session types: {sessions_table['session_type'].unique()}")

observatory_session_id = sessions_table[
    sessions_table['session_type']=='brain_observatory_1.1'].index[0]
connectivity_session_id = sessions_table[
    sessions_table['session_type']=='functional_connectivity'].index[0]
connectivity_session = cache.get_session_data(connectivity_session_id)
observatory_session = cache.get_session_data(observatory_session_id)
print(f'Loaded Brain Observatory session {observatory_session_id}',
      f'and Functional Connectivity session {connectivity_session_id}.')

print('Brain Observatory session stimulus presentations:')
observatory_session.get_stimulus_parameter_values()

print('Connectivity session stimulus presentations:')
connectivity_session.get_stimulus_parameter_values()
# -

# # Load original data and plot example raster

# +
stimulus_type = 'drifting_gratings'
structure = 'VISal'

# Choose example units and stimulus presentations
selected_unit_ids = session.units[
    session.units['ecephys_structure_acronym'] == structure].index.values
drifting_gratings_presentation_ids = session.stimulus_presentations.loc[
    (session.stimulus_presentations['stimulus_name'] == stimulus_type)
].index.values

# Get spike times for selected units and stimulus presentations
times = session.presentationwise_spike_times(
    stimulus_presentation_ids=drifting_gratings_presentation_ids,
    unit_ids=selected_unit_ids
)
times.head()

times_some = times[times['unit_id'] % 4 == 0]

# Plot spike raster for the first drifting grating presentation
first_drifting_grating_presentation_id = times_some[
    'stimulus_presentation_id'].values[0]
plot_times = times_some[
    times_some['stimulus_presentation_id'] == first_drifting_grating_presentation_id]
fig = raster_plot(plot_times, title='spike raster for stimulus presentation'
    f' {first_drifting_grating_presentation_id}')
plt.show()

# Save dataframe to compare with h5 data in the next cells
plot_times.to_csv('_temp_spike_times.csv')
# -

# # Load binned data from h5 files
#
# # ! Environment should be switched to `xarray-env` before running this cell

# +
import os

import matplotlib.pyplot as plt
import pandas as pd

# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# %config InteractiveShell.ast_node_interactivity = 'all'

# +
session_id = 798911424
stimulus_type = 'drifting_gratings'
structure = 'VISal'

DATA_DIR = Path('../data/02_stimulus_types')
h5_file = DATA_DIR / f'{stimulus_type}.h5'
dt = xr.open_datatree(h5_file)
print("DataTree structure:", dt)
dt
# -

# Get spike data DataArray
spike_data = dt[f'session_{session_id}'][structure]['spike_data']['spike_data']
print("Dataset structure:", spike_data)
spike_data

# # Plot raster from loaded binned data and compare with original data

# +
import temp_Allen_data.docs.plot_spikes_over_bins as plot_spikes_over_bins

# Reload spike times from CSV for comparison
times = pd.read_csv('_temp_spike_times.csv')
# Chose same units in binned data
spikes = spike_data.sel(unit_id=times.unit_id.unique())

plot_spikes_over_bins.main(spikes, times)
# -

# Delete temporary CSV file
os.remove('_temp_spike_times.csv')
