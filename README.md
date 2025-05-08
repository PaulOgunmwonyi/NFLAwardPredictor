Notes:

NFL data collected from:
- https://pypi.org/project/nfl-data-py/
- REQUIRES PYTHON VERSION < 13

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