import logging
import sys
from pathlib import Path

import pandas as pd
import xarray as xr

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stderr),
                              logging.FileHandler("logs/run.log")
                            ])
log = logging.getLogger()

in_dir = Path("data/02_stimulus_types")
out_dir = Path("data")
rows = []

h5_files = list(in_dir.glob("*.h5"))
for i, f in enumerate(h5_files):
    log.info(f"Processing file {i+1}/{len(h5_files)}: {f.name}")
    stimulus_type = f.stem
    dt = xr.open_datatree(f)
    for session_name, s in dt.children.items():
        for brain_structure, bs in s.children.items():
            session_id = session_name.removeprefix("session_")

            has_gaze_data = 'gaze_data' in list(bs.children.keys())

            spike_data_sizes = bs["spike_data"].ds.sizes
            n_presentations = spike_data_sizes["presentation_id"]
            n_units = spike_data_sizes["unit_id"]

            rows.append([
                stimulus_type, session_id, brain_structure,
                n_presentations, n_units,
                has_gaze_data])
    dt.close()

out = out_dir / "combined_statistics.csv"
pd.DataFrame(
    rows,
    columns=["stimulus_type", "session_id", "brain_structure",
             "n_presentations", "n_units",
             "has_gaze_data"],
).to_csv(out, index=False)
