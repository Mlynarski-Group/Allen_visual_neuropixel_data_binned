[33mcommit 5227253872387e9f44d6ec3054de0e867586c678[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmaster[m[33m)[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Jan 20 12:27:19 2026 +0100

    [DATALAD RUNCMD] Generate presentations.csv properly concatenated between session types
    
    === Do not change lines below ===
    {
     "chain": [],
     "cmd": "bash -lc '/home/ephys03/.conda/envs/allensdk-pure/bin/python code/0_access_stim_params.py'",
     "exit": 0,
     "extra_inputs": [],
     "inputs": [],
     "outputs": [],
     "pwd": "."
    }
    ^^^ Do not change lines above ^^^

[33mcommit 853f3928b57980b77abb1b5c781678fee025830a[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Jan 20 12:01:40 2026 +0100

    Update datalad run message in datalad_wapper

[33mcommit 14d032fd3a910daa863b43b6848777e1cfc50e5e[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Jan 20 11:59:02 2026 +0100

    Fix creating presentations.csv with varying number of columns

[33mcommit fb481033099c152249d7d82eee5aebd10c0167ce[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Fri Jan 16 18:25:32 2026 +0100

    [DATALAD RUNCMD] Create table of stimulus presentations
    
    === Do not change lines below ===
    
     "chain": [],
     "cmd": "bash -lc '/home/ephys03/.conda/envs/allensdk-pure/bin/python code/0_access_stim_params.py'",
     "exit": 0,
     "extra_inputs": [],
    
     "inputs": [],
     "outputs": [],
     "pwd": "."
    }
    ^^^ Do not change lines above ^^^

[33mcommit 5a582177fcaf61ec86eb35a359d782c2e6d6cd66[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Fri Jan 16 17:58:35 2026 +0100

    Modify datalad_wrapper.sh and cmd call to better control background process

[33mcommit f09d0f49ebe8488b1f94ba839ac40f76e97ecbbb[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Fri Jan 16 17:38:41 2026 +0100

    Add 0_access_stim_params.py

[33mcommit 55bee06ffdfb71d138e213f0bf4c08a156955259[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Fri Jan 16 02:21:01 2026 +0100

    Update datalad_wrapper to run combine_by_stimulus.py

[33mcommit 068e32ab77f0872650ee967bcae2926b941afd98[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Jan 15 23:31:37 2026 +0100

    Reload data with annex

[33mcommit e07096ab5e1aad543deeec5af3715c34d2aceec6[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Jan 15 20:47:31 2026 +0100

    Add .gitattributes: always annex data/ and all binary files

[33mcommit b2b316245017aa3f34bc4c88a4e813088e569437[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Dec 18 02:20:08 2025 +0100

    Rename protocol into README

[33mcommit bdc157c8b9adbf90eb3f87ea7ee70c196ea9eb7e[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Dec 18 02:18:16 2025 +0100

    Update protocol

[33mcommit 32e68b02d43c1f06dd04cbd462aa87e70d4047ca[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Dec 18 01:43:40 2025 +0100

    Fix paths and logging

[33mcommit b26dcdf90b45e20b31d989b18187adb919295f76[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Dec 18 01:35:19 2025 +0100

    Script combine_by_stimulus.py

[33mcommit c841b69c68b0d79afe9ee80ea7ab79f6633cdbc1[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Thu Dec 18 01:33:51 2025 +0100

    Add units.csv to data

[33mcommit 383115be302098f145306c4dde92d3f5d92ea230[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Dec 16 21:12:12 2025 +0100

    [DATALAD RUNCMD] Create sessions-presentations
    
    === Do not change lines below ===
    {
     "chain": [],
     "cmd": "python code/access_allen_data.py",
     "exit": 0,
     "extra_inputs": [],
     "inputs": [],
     "outputs": [],
     "pwd": "."
    }
    ^^^ Do not change lines above ^^^

[33mcommit 40f94fa94b6518cf84109e31bfe6c58cc266fe57[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Dec 16 11:25:14 2025 +0100

    Read and write list of completed sessions

[33mcommit 305b48de31f6c24002c879be1160534d71f3393b[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Dec 16 10:57:45 2025 +0100

    Update protocol

[33mcommit 5f3c81ec5cf14409c5ef5c084d7457ba7fa5152a[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Dec 16 10:55:57 2025 +0100

    Filter out 'null' presentations in dot_motion

[33mcommit 709c9a26f2cc6e9630b1e4b4c092fa240e96697a[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Dec 16 10:49:53 2025 +0100

    Save 27 processed sessions 715093703-761418226

[33mcommit 628c413163c8baf2cbe151ded29ea69a9706b8db[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Tue Dec 16 10:29:04 2025 +0100

    Quiet allensdk noisy logger

[33mcommit 1b176d7c7b1e9ca91f6192baf24a4e3cb5098196[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 23:24:51 2025 +0100

    Fix logging

[33mcommit 16d13f66d8de58f478ccad54e2c38a8e8506325f[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 23:16:32 2025 +0100

    Filter out natural scenes with frame=-1 (blank)

[33mcommit 93d578a4c8fa49bc950adeccabbc85786fb50302[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 23:15:55 2025 +0100

    Add list of invalid stimulus_name substrings

[33mcommit ea18f0ebb6421403156f4ce4e2e8fd4e43aba612[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 23:14:50 2025 +0100

    Skip completed sessions (update list manually)

[33mcommit 7b50551d313f57e7701fac99bbcfe5c80e3610f2[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 23:00:39 2025 +0100

    Update protocol

[33mcommit 34324eac81bfcfeb44ff8d2db716374eda52af0b[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 20:18:35 2025 +0100

    Fix movie aggregation

[33mcommit 13deb94691258dacab3adecdee1601ed4348da16[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 17:24:52 2025 +0100

    Add logging to code

[33mcommit 28e1f4a55ec8634dc3055e8e18386290aad2ab1f[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 16:15:11 2025 +0100

    Create datalad_wrapper.sh to run code remotely

[33mcommit d21199547b6514b224ad0a80cddd6f7b6c683369[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 12:36:36 2025 +0100

    Add /logs to .gitignore

[33mcommit e632177a2e83af6a98206962320cd3637e45cc90[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 12:22:08 2025 +0100

    Exclude /data from .gitignore

[33mcommit eb34bba3003746b1c31bad4421a05c5f4bb1e89d[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 11:29:34 2025 +0100

    Add /protocols folder

[33mcommit 7d4501ac2641903d8df8a4bdfc150c81932f6513[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 11:28:07 2025 +0100

    Filter out blank presentations in gratings

[33mcommit 8c07db156f798dd4ff38fb3bf26c2dd6391b1c90[m
Author: Arseniy Pelevin <arsenii.pelevin@campus.lmu.de>
Date:   Mon Dec 15 04:35:52 2025 +0100

    Initial commit
