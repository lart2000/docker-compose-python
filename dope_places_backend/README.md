# Dope Places

## Dependencies:

#### Common.in:

1. mysqlclient

    - Install `mysql` on your system

#### Develop.in:

1. pygraphviz

    - Install `graphviz` on your system
    - In case you don't have `graphviz`, remove `graphviz` and `pygraphviz` from `requirements/develop.in`

## Development

- `git clone git@gitlab.com:helpse/dope_places_backend.git` # Clone the repository
- `cd dope_places_backend`
- `virtualenv venv -p /path/to/python` # Create virtualenv
- `. venv/Scripts/activate` # Activate virtualenv
- `pip install pip-tools`
- `pip-sync requirements-20190117.develop` # Synchronize the dependencies and versions of your virtual environment with those of the generated file
- Create a `.env` file from `.env.example` and populate variables
- Set `ENVIRONMENT_MODULE` in `.env` file, alternatives are: `develop`, `testing`, `staging` and `production`.
- `python manage.py loaddata countries`
- `python manage.py runserver`

## Run tests and generate html coverage code report

- `coverage run --source='.' manage.py test && coverage html`
- Open `htmlcov/index.html` in your browser
