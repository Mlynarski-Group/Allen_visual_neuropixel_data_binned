Cache loaded.
Found 58 sessions.
Processing session 715093703(1/58)
/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/hdmf/spec/namespace.py:590: UserWarning: Ignoring the following cached namespace(s) because another version is already loaded:
core - cached version: 2.2.2, loaded version: 2.7.0
The loaded extension(s) may not be compatible with the cached extension(s) in the file. Please check the extension documentation and ignore this warning if these versions are compatible.
  self.warn_for_ignored_namespaces(ignored_namespaces)

Session 715093703 loaded.
This ecephys session '715093703' has no eye tracking data. (NWB error: "'raw_gaze_mapping' not found in processing of NWBFile 'root'.")
Obtained running speed and gaze data.
        Processing stimulus type: gabors
                Computed spike counts.
                Computed running speed.
                Computed gaze data.
                Files for stimulus type gabors saved.
        Processing stimulus type: flashes
                Computed spike counts.
                Computed running speed.
                Computed gaze data.
                Files for stimulus type flashes saved.
        Processing stimulus type: drifting_gratings
                Computed spike counts.
                Computed running speed.
                Computed gaze data.
Traceback (most recent call last):
  File "/storage2/arash/teaching/neuropy/arsenii/temp_Allen_data/code/access_allen_data.py", line 222, in <module>
    main()
  File "/storage2/arash/teaching/neuropy/arsenii/temp_Allen_data/code/access_allen_data.py", line 214, in main
    process_session(cache, session_id)
  File "/storage2/arash/teaching/neuropy/arsenii/temp_Allen_data/code/access_allen_data.py", line 48, in process_session
    process_stimulus_type(
  File "/storage2/arash/teaching/neuropy/arsenii/temp_Allen_data/code/access_allen_data.py", line 73, in process_stimulus_type
    stimuli = type_presentations.astype(np.float32).to_xarray()
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/generic.py", line 6240, in astype
    new_data = self._mgr.astype(dtype=dtype, copy=copy, errors=errors)
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/internals/managers.py", line 448, in astype
    return self.apply("astype", dtype=dtype, copy=copy, errors=errors)
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/internals/managers.py", line 352, in apply
    applied = getattr(b, f)(**kwargs)
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/internals/blocks.py", line 526, in astype
    new_values = astype_array_safe(values, dtype, copy=copy, errors=errors)
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/dtypes/astype.py", line 299, in astype_array_safe
    new_values = astype_array(values, dtype, copy=copy)
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/dtypes/astype.py", line 230, in astype_array
    values = astype_nansafe(values, dtype, copy=copy)
  File "/home/ephys03/.conda/envs/allensdk/lib/python3.9/site-packages/pandas/core/dtypes/astype.py", line 170, in astype_nansafe
    return arr.astype(dtype, copy=True)
ValueError: could not convert string to float: 'null'