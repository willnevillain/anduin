# Anduin: The Amazon of Middle-Earth

## Bootstrap
Python 3.7.6 required, recommended to install via `pyenv`.
```bash
pipenv --python 3.7.6
pipenv install
```

## Running Server
With the virtualenv activated (probably via `pipenv shell`):
```bash
export FLASK_APP=/path/to/entrypoint.py
flask run
```

## Endpoints
```
GET /api/users
GET /api/users/:id
GET /api/users/:id/inventory
POST /api/offers
POST /api/offers/:id/accept
POST /api/offers/:id/reject
```
