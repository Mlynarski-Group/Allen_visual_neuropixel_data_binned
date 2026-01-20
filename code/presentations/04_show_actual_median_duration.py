import pandas as pd

input_path = 'data/presentations/02_presentations_whole_movies.csv'

pres = pd.read_csv(input_path)
names = pres['stimulus_name'].unique()

for name in names:
    pres_type = pres[pres['stimulus_name'] == name]
    durations = pres_type['duration']
    type_median = durations.median()

    print(f"{name}: {type_median:.4f} s")
