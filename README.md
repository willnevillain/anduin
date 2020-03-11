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

## Possible Areas to Scale
1. Table to track enumerated races (currently validated in models/users.py)
2. Table to track enumerated weapons (currently validate in models/weapons.py)
3. Dedicated models for many-to-many tables (currently defined in models/offers.py)

