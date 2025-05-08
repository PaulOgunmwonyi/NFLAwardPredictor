from django.http import HttpResponse
from django.shortcuts import render
import nfl_data_py as nfl
import pandas as pd

def home(request):
    qb_qbr = nfl.import_qbr(range(2022,2024))
    url = "https://github.com/nflverse/nflverse-data/releases/download/espn_data/qbr_season_level.parquet"
    curr_qbr = pd.read_parquet(url).loc[lambda x: x.season == 2024].reset_index(drop=True)
    filtered_qb_qbr = qb_qbr[qb_qbr['qb_plays'] > 50]
    filtered_curr_qbr = curr_qbr[curr_qbr['qb_plays'] > 50]

    context = {
        'qb_qbr': filtered_qb_qbr.to_dict(orient='records'),
        'curr_qbr': filtered_curr_qbr.to_dict(orient='records'),
    }
    return render(request, 'home.html', context)

def about(request):
    return HttpResponse("This is the About page for the NFL Award Predictor.")