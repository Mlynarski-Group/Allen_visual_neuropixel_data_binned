import pandas as pd

input_path = 'data/presentations/02_presentations_whole_movies.csv'
output_path = 'presentation/presentations_median_durations.csv'

pres = pd.read_csv(input_path)
names = pres['stimulus_name'].unique()

rows = []

for name in names:
    pres_type = pres[pres['stimulus_name'] == name]
    durations = pres_type['duration']
    type_median = durations.median()

    rows.append((name, type_median))
    print(f"{name}: {type_median:.4f} s")

df = pd.DataFrame(rows, columns=['stimulus_name', 'median_duration'])
df.to_csv(output_path, index=False)
