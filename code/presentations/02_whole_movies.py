import pandas as pd


def whole_movie_presentations(df):
    frames = df['frame']
    new_movie = frames.diff().fillna(1) < 0
    df.loc[:, 'movie_group'] = new_movie.cumsum()
    agg = df.groupby(['session_id', 'movie_group', 'stimulus_name']).agg(
        stimulus_presentation_id=('stimulus_presentation_id', 'first'),
        stimulus_block=('stimulus_block', 'first'),
        start_time=('start_time', 'min'),
        stop_time=('stop_time', 'max'),
        duration=('duration', 'sum')
    )
    return agg

input_path = 'data/presentations/01_presentations_original.csv'
output_path = 'data/presentations/02_presentations_whole_movies.csv'

pres = pd.read_csv(input_path)
movie_pres = pres[pres['stimulus_name'].str.contains('natural_movie')]

movie_pres_whole = whole_movie_presentations(movie_pres)
movie_pres_whole = movie_pres_whole.reset_index().drop(columns=['movie_group'])

other_pres = pres[~pres['stimulus_name'].str.contains('natural_movie')]

all_pres = pd.concat([other_pres, movie_pres_whole], ignore_index=True)

# Sort to preserve original order
sess_order = pres['session_id'].drop_duplicates()
all_pres['session_id'] = pd.Categorical(
    all_pres['session_id'], categories=sess_order, ordered=True)
all_pres = all_pres.sort_values(['session_id', 'stimulus_presentation_id'],
                                kind='stable')

all_pres.to_csv(output_path, index=False)
