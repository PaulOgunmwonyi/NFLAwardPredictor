from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import joblib
import os
from .models import data
from .data import record_data

def home(request):
    # data for displaying past MVPs
    filtered_data = data[data['mvp'] == 1].to_dict(orient='records')
    prediction = 'Input values for a prediction!'
    graph_url = None

    if request.method == 'POST':
        # load model
        model = joblib.load('nfl_mvp_model.pkl')

        # get input data from the form
        input_data = {
            'wins': int(float(request.POST['wins'])),
            'qbr_total': float(request.POST['qbr_total']),
            'epa_total': float(request.POST['epa_total']),
            'epa_per_play': float(request.POST['epa_per_play']),
            'qb_plays': int(float(request.POST['qb_plays'])),
            'sacks': int(float(request.POST['sacks'])),
            'passing_tds': int(float(request.POST['passing_tds'])),
            'interceptions': int(float(request.POST['interceptions'])),
            'passing_yards': int(float(request.POST['passing_yards'])),
            'passer_rating': float(request.POST['passer_rating']),
            'rushing_yards': int(float(request.POST['rushing_yards'])),
            'rushing_tds': int(float(request.POST['rushing_tds'])),
        }
        input_df = pd.DataFrame([input_data])
        probabilities = model.predict_proba(input_df)
        prediction = 'Likely MVP' if probabilities[0][1] >= 0.3 else 'Unlikely MVP'

        # Create a bar graph
        mvp_data = filtered_data[6]
        categories = list(input_data.keys())
        user_values = [input_data[stat] for stat in categories]
        mvp_values = [mvp_data[stat] for stat in categories]

        plt.figure(figsize=(10, 6))
        bar_width = 0.35
        x = range(len(categories))

        plt.bar(x, mvp_values, width=bar_width, label='MVP', color='blue', alpha=0.7)
        plt.bar([i + bar_width for i in x], user_values, width=bar_width, label='User Input', color='orange', alpha=0.7)

        plt.yscale('log')

        plt.xlabel('Categories')
        plt.ylabel('Values')
        plt.title('Comparison of MVP vs User Input')
        plt.xticks([i + bar_width / 2 for i in x], categories, rotation=45, ha='right')
        plt.legend()

        # Ensure the media directory exists
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        # Save the graph as an image
        graph_path = os.path.join(settings.MEDIA_ROOT, 'comparison_graph.png')
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

        # Store the graph URL for rendering in the template
        graph_url = os.path.join(settings.MEDIA_URL, 'comparison_graph.png')

        # Store the prediction and graph in the session and redirect
        request.session['prediction'] = prediction
        request.session['graph_url'] = graph_url
        return redirect('home') 

    # Retrieve the prediction from the session (if available)
    if 'prediction' in request.session:
        prediction = request.session.pop('prediction')  
    if 'graph_url' in request.session:
        graph_url = request.session.pop('graph_url')

    context = {
        'filtered_data': filtered_data,
        'record_data': record_data,
        'prediction': prediction,
        'graph_url': graph_url,
    }
    return render(request, 'home.html', context)