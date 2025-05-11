# NFL Awards Predictor
As a passionate NFL fan who enjoys analyzing player film and debating MVP contenders each season, I set out to create a tool that mirrors the logic behind MVP predictions—similar to those used by betting algorithms—but powered by user input. The result is a machine learning model that predicts the NFL MVP with 87% accuracy across the past seven seasons, with the only miss being 2021 Tom Brady, who finished second in MVP voting. Users can enter hypothetical quarterback stats, and the model will evaluate whether those numbers would likely secure the MVP title in today’s NFL landscape.

For example, Joe Burrow's stellar 2024 campaign filled up the stat sheets but he severely lacked in the wins column so inputting his data only gives a 12% probability of being an MVP. On the flip side, one of the greatest overall qb seasons of all time, 2013 Peyton Manning, gets an overwhelming 75% probability of being an MVP. For those unfamiliar with NFL advanced stats, feel free to use the displayed values as examples.



Notes to self:

NFL data collected from:
- https://pypi.org/project/nfl-data-py/
- REQUIRES PYTHON VERSION < 13
- https://rowzero.io/blog/nfl-data-py-in-a-spreadsheet-nfl-stats

To Run:
- source venv/bin/activate
- python3 manage.py runserver

For adding dependencies:
- source venv/bin/activate
- pip install streamlit #example command
- streamlit --version
- pip freeze > requirements.txt
- deactivate