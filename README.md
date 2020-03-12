# Anduin: The Amazon of Middle-Earth

## TL;DR
1. API contract definitions are in `anduin/views/`.
2. ORM models are in `anduin/models/`, DB schema is versioned and can be found in `migrations/versions/`.

## Requirements

##### Python 3.7.6
Recommended to install via [pyenv](https://github.com/pyenv/pyenv).
```bash
pyenv install 3.7.6
```

##### Pipenv
Recommended tool for dependency and virtualenv management.
```bash
brew install pipenv
```

##### Postgres
```bash
brew install postgres
```

##### Docker
Ensure it is running by checking Menu Bar.
```bash
brew cask install docker
```

## Bootstrapping

Export path to Flask app entrypoint - required for any `flask` commands to work.
```bash
export FLASK_APP=/path/to/entrypoint.py
```

Create virtualenv and install dependencies into it.
```bash
pipenv --python 3.7.6
pipenv install
```

Stand up Postgres container, create dev and test databases.
```bash
docker run --name postgres-moria -e POSTGRES_PASSWORD=<use-LOCAL_DB_PASSWORD-from-config.py> -p 5432:5432 -d postgres
docker exec postgres-moria psql -U postgres -c 'create database anduin_dev;'
docker exec postgres-moria psql -U postgres -c 'create database anduin_test;'
```

Migrate DB schema into created databases.
```bash
flask db upgrade
```

## Commands
All require virtualenv activated (probably via `pipenv shell`) and `FLASK_APP` env var exported.

### Run Server
```bash
flask run
```

### Backfill Data
```bash
flask backfill
```

### Empty Database Tables
Keeps schema intact, does not require re-migrating DB.
```bash
flask empty
```

### Running Tests
```bash
pytest
```


### Troubleshooting

##### Command not found: flask
You're not in the virtual environment.

Option A: Run all flask commands with the virtualenv activated.
```bash
pipenv shell
# Now you can run commands
```

OR

Option B: Run all flask commands preceded by `pipenv run --`, which will run the command in the virtualenv. E.g.
```bash
pipenv run -- flask db init
```

##### Could not locate a Flask application
Don't forget to set the `FLASK_APP` environment variable.
```bash
export FLASK_APP=/path/to/entrypoint.py
```

##### Unable to migrate DB
Nuke the `migrations/` folder and run the following commands:
```bash
flask db init
flask db migrate
flask db upgrade
```

If the above doesn't work, please re-clone the repo to get back to square one, then create an issue.

##### Psycopg2 fails to install
Export these environment variables to correctly link `openssl`, then try again.
```bash
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

## Crude Documentation

### Endpoints
```
GET /api/users
GET /api/users/:id
GET /api/users/:id/inventory
POST /api/offers
GET /api/offers/:id
POST /api/offers/:id/accept
POST /api/offers/:id/reject
```

### Areas to Scale
1. Table to track enumerated races (currently validated in models/users.py against constants)
2. Table to track enumerated weapons (currently validated in models/weapons.py against constants)
3. Maybe dedicated models for many-to-many tables (association tables currently defined in models/offers.py)
4. Backfill and empty scripts are narrow scoped and would require refactoring to scale to more tables with more complex relationships
5. Incoming request body schema validation and deserialization
6. Restructure project into [component based style](https://github.com/goldbergyoni/nodebestpractices/blob/master/sections/projectstructre/breakintcomponents.md) rather than MVC style - better for increased scope or if breaking up into individual microservices.

