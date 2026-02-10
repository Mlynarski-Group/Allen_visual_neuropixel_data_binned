import pandas as pd

pres_all = pd.read_csv('data/presentations/02_presentations_whole_movies.csv')
pres_filt = pd.read_csv('data/presentations/03_presentations_filtered_by_duration.csv')
output_path = 'docs/presentations_filtered_summary.csv'

names = pres_all['stimulus_name'].unique()

rows = []

for name in names:
    name_dur = pres_all[pres_all['stimulus_name'] == name]['duration']
    num_pres = len(name_dur)
    name_dur_filt = pres_filt[pres_filt['stimulus_name'] == name]['duration']
    num_pres_filt = len(name_dur_filt)

    rows.append((name, num_pres, num_pres_filt, num_pres - num_pres_filt,
                 round((num_pres - num_pres_filt) / num_pres * 100, 2)))
    print(f"{name}: {num_pres} - {num_pres_filt} = {num_pres - num_pres_filt}"
          f" ({(num_pres - num_pres_filt) / num_pres * 100:.2f}%)")

df = pd.DataFrame(rows, columns=['stimulus_name', 'num_presentations_before',
                                 'num_presentations_after', 'num_presentations_removed',
                                 'percent_presentations_removed'])
df.to_csv(output_path, index=False)
