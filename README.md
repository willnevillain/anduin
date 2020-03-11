# Anduin: The Amazon of Middle-Earth

## Bootstrap
Python 3.7.6 required, recommended to install via `pyenv`.
```bash
pipenv --python 3.7.6
pipenv install
```

You'll also need a Postgres container stood up with DBs provisioned to run app or tests locally.
```bash
docker run --name postgres-moria -e POSTGRES_PASSWORD=<use-LOCAL_DB_PASSWORD-from-config.py> -d postgres
docker exec postgres-barrel psql -U postgres -c 'create database anduin_dev;'
docker exec postgres-barrel psql -U postgres -c 'create database anduin_test;'
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

## Areas to Scale
1. Table to track enumerated races (currently validated in models/users.py against constants)
2. Table to track enumerated weapons (currently validated in models/weapons.py against constants)
3. Dedicated models for many-to-many tables (association tables currently defined in models/offers.py)

## Concessions
1. App is structured in MVC style rather than [component based style](https://github.com/goldbergyoni/nodebestpractices/blob/master/sections/projectstructre/breakintcomponents.md) due to the small scale and narrow scoping. If this app were to begin increasing in scale, become a foundation for a monolithic backend, or need to be broken up into individual microservices, then refactoring the project structure would be the first item on the list.
2. DB Schema is not currently being versioned, but is rather being created dynamically at app startup via `db.create_all()`. This is fine, but unsustainable at scale. Were the schema to change at all, versioning via a tool like `alembic` would be introduced prior to changes being implemented.

