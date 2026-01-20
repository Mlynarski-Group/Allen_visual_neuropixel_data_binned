import pandas as pd

input_path = 'data/presentations/02_presentations_whole_movies.csv'
output_path = 'data/presentations/03_presentations_filtered_by_duration.csv'

pres = pd.read_csv(input_path)
names = pres['stimulus_name'].unique()

pres_filtered = pd.DataFrame()

for name in names:
    deviation_threshold = 0.01 if 'natural_movie' in name else 0.001

    pres_type = pres[pres['stimulus_name'] == name]

    durations = pres_type['duration']
    type_median = durations.median()

    pres_filtered = pd.concat([
        pres_filtered,
        pres_type[
            (abs(durations - type_median) < deviation_threshold)
        ]
    ], ignore_index=True)

# Sort to preserve original order
sess_order = pres['session_id'].drop_duplicates()
pres_filtered['session_id'] = pd.Categorical(
    pres_filtered['session_id'], categories=sess_order, ordered=True)
pres_filtered = pres_filtered.sort_values(['session_id'], kind='stable')

pres_filtered.to_csv(output_path, index=False)
