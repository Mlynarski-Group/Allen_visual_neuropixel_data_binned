import gc
import logging
import os
from pathlib import Path

import pandas as pd
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    handlers=[logging.FileHandler("logs/params_table.log")])
log = logging.getLogger()
# Quiet noisy allensdk logger
lg = logging.getLogger("call_caching")
for h in lg.handlers[:]:
    lg.removeHandler(h)
lg.setLevel(logging.WARNING)

# Load cache
input_dir = "/storage2/wp7/allendata"
manifest_path = os.path.join(input_dir, "manifest.json")
cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)
log.info("Cache loaded.")

# Access session IDs
sessions_table = cache.get_session_table()
session_ids = sessions_table.index.values.tolist()
log.info(f"Found {len(session_ids)} sessions.")

# Define output file and delete if exists
out_dir = Path("data")
out = out_dir / "presentations.csv"
out.unlink(missing_ok=True)

# Define invalid stimulus types
invalid = ["spontaneous", "shuffled", "invalid"]
invalid_pattern = "|".join(invalid)

pres_all = pd.DataFrame()

for i, session_id in enumerate(session_ids, 1):
    session = cache.get_session_data(session_id)
    log.info(f"Session {session_id} loaded ({i}/{len(session_ids)}).")

    pres = session.stimulus_presentations

    # Filter out invalid stimulus presentation types
    pres = pres[~pres["stimulus_name"].str.contains(invalid_pattern, regex=True)]

    # Move 'stimulus_presentation_id' to first column and add 'session_id' column
    pres = pres.reset_index()
    pres.insert(0, "session_id", session_id)

    pres_all = pd.concat([pres_all, pres], axis=0, ignore_index=True)

    del session
    gc.collect()

pres_all.to_csv(out, index=False)
log.info("Done.")
