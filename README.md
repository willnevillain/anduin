# Anduin: The Amazon of Middle-Earth

## TL;DR
1. API contract definitions are in `anduin/views/`.
2. App registration and error handlers defiend in `anduin/app.py`.
3. The tests under `tests/integration_tests/views/` are probably of interest.
4. ORM models are in `anduin/models/`, DB schema is versioned and can be found in `migrations/versions/`.
5. Things that still need improving are noted at the bottom of this README, but I'm happy with the way it turned out overall.

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
All require:
1. virtualenv activated (probably via `pipenv shell`)
2. `FLASK_APP` env var exported.
3. run from the root of the project

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
python -m pytest tests/
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

### Areas to Scale and Improve
1. Table to track enumerated races (currently validated in models/users.py against constants)
2. Table to track enumerated weapons (currently validated in models/weapons.py against constants)
3. Maybe dedicated models for many-to-many tables (association tables currently defined in models/offers.py)
4. Backfill and empty scripts are narrow scoped and would require refactoring to scale to more tables with more complex relationships
5. Incoming request body schema validation and deserialization
6. Restructure project into [component based style](https://github.com/goldbergyoni/nodebestpractices/blob/master/sections/projectstructre/breakintcomponents.md) rather than MVC style - better for increased scope or if breaking up into individual microservices.
7. Composition of function calls in controllers rather than OO method chaining will make writing unit test cases easier, allowing less reliance on integration / e2e tests for heavy DB logic
8. More efficient and repeatable DB-object validation pattern - validating new offer on `POST /offers` makes n DB calls where n is number of weapons passed in. Validation function also not standardized (since it's the only place in codebase with validation at this time). It's also ugly, but gets the job done. It can be cleaned up to not make redundant DB calls with the create function, but that would also up complexity a bit. Tradeoffs.
9. Assumption is made at this time that transactions with no weapons can occur without error (though a bit weird and useless admittedly), and that transactions where one user is giving away weapons to another is also valid.
10. We have absolutely no logging solution or form of observability.
11. Less sunny-day paths on testing - need tests that handle when DB errors out or becomes unaccessible.
