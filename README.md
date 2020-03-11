# Anduin: The Amazon of Middle-Earth

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

## Running Server
With the virtualenv activated (probably via `pipenv shell`):
```bash
flask run
```

## Running Tests
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
POST /api/offers/:id/accept
POST /api/offers/:id/reject
```

### Areas to Scale
1. Table to track enumerated races (currently validated in models/users.py against constants)
2. Table to track enumerated weapons (currently validated in models/weapons.py against constants)
3. Dedicated models for many-to-many tables (association tables currently defined in models/offers.py)

### Concessions
1. App is structured in MVC style rather than [component based style](https://github.com/goldbergyoni/nodebestpractices/blob/master/sections/projectstructre/breakintcomponents.md) due to the small scale and narrow scoping. If this app were to begin increasing in scale, become a foundation for a monolithic backend, or need to be broken up into individual microservices, then refactoring the project structure would be the first item on the list.

