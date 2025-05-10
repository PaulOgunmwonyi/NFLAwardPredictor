from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import joblib
from .models import data
from .data import record_data
import json

def home(request):
    filtered_data = data[data['mvp'] == 1].to_dict(orient='records')

    context = {
        'filtered_data': filtered_data,
        'record_data': record_data,
    }
    return render(request, 'home.html', context)

def about(request):
    model = joblib.load('nfl_mvp_model.pkl')
    input_data = pd.DataFrame([{
        'wins': 13,'qbr_total': 74.1,'epa_total': 134.8,             
        'epa_per_play': .1352, 'qb_plays': 997,'sacks': 30,   'passing_tds': 37, 'interceptions': 4, 'passing_yards': 4115, 'passer_rating': 111.9, 
        'rushing_yards': 101, 'rushing_tds': 1
    }])
    probabilities = model.predict_proba(input_data)
    print(probabilities)
    prediction = 1 if probabilities[0][1] >= 0.3 else 0

    return HttpResponse(f"Prediction: {'Best Player' if prediction == 1 else 'Not Best Player'}")