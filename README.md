# KOMAJI
FastAPI based backend for small projects.

## Deployment
* dev deployment - docker-compose. Run `docker-compose -f "docker-compose.yaml" up -d --build` to deploy.
    * upon first deployment run `alembic revision --autogenerate` in the container console
    * check `http://localhost:5003/docs` for api docs
    * check `http://localhost:5050/` for pgadmin
* production deployment - kubernetes (work in progress)

All config values must be stored in `config.env` in project root. It must have folowing values:

    JWT_SECRET_KEY
    SECRET_KEY
    FLASK_ENV
    FLASK_APP
    FLASK_DEBUG

    POSTGRES_DB
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_HOST
    POSTGRES_PORT

    PGADMIN_DEFAULT_EMAIL
    PGADMIN_DEFAULT_PASSWORD