from django.db import models
import nfl_data_py as nfl
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from .data import record_data

# Load the data from nfl_data_py
qb_qbr = nfl.import_qbr(range(2018,2024))
url = "https://github.com/nflverse/nflverse-data/releases/download/espn_data/qbr_season_level.parquet"
curr_qbr = pd.read_parquet(url).loc[lambda x: x.season == 2024].reset_index(drop=True)
qb_data = nfl.import_ngs_data('passing', range(2018, 2025))
sack_data = nfl.import_seasonal_data(range(2018, 2025))

# Filter the data and combine the 3 data sources 
id_df = nfl.import_ids()
id_df = id_df[['gsis_id','name']]
sack_data = pd.merge(sack_data, id_df, left_on = 'player_id', right_on = 'gsis_id', how ='left')
filtered_qb_qbr = qb_qbr[(qb_qbr['qb_plays'] > 100) & (qb_qbr['season_type'] == 'Regular')]
filtered_curr_qbr = curr_qbr[(curr_qbr['qb_plays'] > 100) & (curr_qbr['season_type'] == 'Regular')]
data = pd.concat([filtered_qb_qbr, filtered_curr_qbr])
record_df = pd.DataFrame(record_data)
data = data.merge(record_df, how='left', left_on=['team', 'season'], right_on=['team', 'year'])
data = data.drop(columns=['year'])
data = data[[
    'season',         
    'name_first',      
    'name_last',       
    'team',           
    'wins',            
    'losses',          
    'qbr_total',       
    'epa_total',          
    'qb_plays'        
]]
data['epa_per_play'] = data['epa_total'] / data['qb_plays']
qb_data_relevant = qb_data[[
    'season', 
    'player_first_name', 
    'player_last_name', 
    'passer_rating',
]]
qb_data_relevant = qb_data_relevant.drop_duplicates(subset=['season', 'player_first_name', 'player_last_name'])
data = data.merge(
    qb_data_relevant,
    how='left',
    left_on=['season', 'name_first', 'name_last'],
    right_on=['season', 'player_first_name', 'player_last_name']
)
data = data.drop(columns=['player_first_name', 'player_last_name'])
data = data.drop_duplicates()
sack_data_relevant = sack_data[[
    'season',
    'name',
    'sacks',
    'passing_tds',
    'passing_yards',
    'interceptions', 
    'rushing_yards',
    'rushing_tds',
]]
sack_data_relevant = sack_data_relevant.drop_duplicates(subset=['season', 'name'])
data['full_name'] = data['name_first'] + ' ' + data['name_last']
data = data.merge(
    sack_data_relevant,
    how='left',
    left_on=['season', 'full_name'],
    right_on=['season', 'name']
)
data = data.drop(columns=['name', 'full_name'])
data = data.drop_duplicates()

# adding data to important players left out (MVP candidates)
data.loc[(data['season'] == 2024) & (data['name_first'] == 'Josh') & (data['name_last'] == 'Allen'), 'passer_rating'] = 101.4
data.loc[(data['season'] == 2023) & (data['name_first'] == 'Josh') & (data['name_last'] == 'Allen'), 'passer_rating'] = 92.2
data.loc[(data['season'] == 2023) & (data['name_first'] == 'Dak') & (data['name_last'] == 'Prescott'), 'passer_rating'] = 105.9

# calculations for MVP
weights = {
    'qbr_total' : .5,
    'epa_total' : .5,
    'epa_per_play' : 25,
    'qb_plays' : .0025,
    'sacks' : -1.5,
    'passing_tds' : .75,
    'interceptions' : -2,
    'passing_yards' : .005,
    'passer_rating' : .5,
    'rushing_yards' : .005,
    'rushing_tds' : .75,
}
data['score'] = (
    np.where(data['wins'] >= 10, 50 , 0) +
    np.where(data['wins'] >= 13, 50 , 0) +
    weights['qbr_total'] * data['qbr_total'] +
    weights['epa_total'] * data['epa_total'] +
    weights['epa_per_play'] * data['epa_per_play'] +
    weights['qb_plays'] * data['qb_plays'] +
    weights['sacks'] * data['sacks'] +  
    weights['passing_tds'] * data['passing_tds'] +  
    weights['interceptions'] * data['interceptions'] +
    weights['passing_yards'] * data['passing_yards'] +  
    weights['passer_rating'] * data['passer_rating'] +
    weights['rushing_yards'] * data['rushing_yards'] +
    weights['rushing_tds'] * data['rushing_tds']
)
data['mvp'] = data.groupby('season')['score'].transform(lambda x: x == x.max()).astype(int)

# Define features and target
features = [
    'wins', 'qbr_total', 'epa_total', 'epa_per_play',
    'qb_plays', 'sacks', 'passing_tds', 'interceptions', 
    'passing_yards', 'passer_rating', 'rushing_yards', 'rushing_tds'
]
target = 'mvp'

# Split the data into training and testing sets
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose a model
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),  # Handle missing values
    ('model', RandomForestClassifier(random_state=42, class_weight='balanced'))  # Train the model
])

# Train the model
pipeline.fit(X_train, y_train)

joblib.dump(pipeline, 'nfl_mvp_model.pkl')