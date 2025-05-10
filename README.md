# NFL Awards Predictor
As a passionate NFL fan who enjoys analyzing player film and debating MVP contenders each season, I set out to create a tool that mirrors the logic behind MVP predictions—similar to those used by betting algorithms—but powered by user input. The result is a machine learning model that predicts the NFL MVP with 87% accuracy across the past seven seasons, with the only miss being 2021 Tom Brady, who finished second in MVP voting. Users can enter hypothetical quarterback stats, and the model will evaluate whether those numbers would likely secure the MVP title in today’s NFL landscape.

Notes to self:

NFL data collected from:
- https://pypi.org/project/nfl-data-py/
- REQUIRES PYTHON VERSION < 13
- https://rowzero.io/blog/nfl-data-py-in-a-spreadsheet-nfl-stats

Requires python, pip, and django to be installed
- https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- https://docs.djangoproject.com/en/5.2/intro/install/
- https://docs.djangoproject.com/en/5.2/topics/install/#installing-official-release

Create a virtual environment: 
- python3 -m venv venv

To Run:
- source venv/bin/activate
- python3 manage.py runserver

For adding dependencies:
- source venv/bin/activate
- pip install streamlit #example command
- streamlit --version
- pip freeze > requirements.txt
- deactivate