from django.http import HttpResponse
from django.shortcuts import render
import nfl_data_py as nfl
import pandas as pd
from .data import record_data
import joblib

def home(request):
    qb_qbr = nfl.import_qbr(range(2022,2024))
    url = "https://github.com/nflverse/nflverse-data/releases/download/espn_data/qbr_season_level.parquet"
    curr_qbr = pd.read_parquet(url).loc[lambda x: x.season == 2024].reset_index(drop=True)

    filtered_qb_qbr = qb_qbr[(qb_qbr['qb_plays'] > 50) & (qb_qbr['season_type'] == 'Regular')]
    filtered_curr_qbr = curr_qbr[(curr_qbr['qb_plays'] > 50) & (curr_qbr['season_type'] == 'Regular')]

    context = {
        'qb_qbr': filtered_qb_qbr.to_dict(orient='records'),
        'curr_qbr': filtered_curr_qbr.to_dict(orient='records'),
        'record_data': record_data,
    }
    return render(request, 'home.html', context)

def about(request):
    model = joblib.load('nfl_mvp_model.pkl')
    input_data = pd.DataFrame([{
        'wins': 14, 'qbr_total': 79, 'epa_total': 200, 'epa_per_play': .1, 'pass': 40, 'run': 15, 
        'qb_plays':1000, 'sacks': 26, 'passing_tds': 41, 'interceptions': 12, 
        'passing_yards': 5250, 'passer_rating': 105.2, 'rushing_yards': 358, 'rushing_tds': 4
    }])
    probabilities = model.predict_proba(input_data)
    print(probabilities)
    prediction = 1 if probabilities[0][1] > 0.3 else 0

    return HttpResponse(f"Prediction: {'Best Player' if prediction == 1 else 'Not Best Player'}")