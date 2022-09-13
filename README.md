# KOMAJI
FastAPI based backend for small projects.

## Deployment
* dev deployment - docker-compose. Run `docker-compose -f "docker-compose.yaml" up -d --build` to deploy.
* production deployment - kubernetes (work in progress)

All config values must be stored in `config.env` in project root. It must have folowing values:

    JWT_SECRET_KEY
    SECRET_KEY
    FLASK_ENV
    FLASK_APP
    FLASK_DEBUG

    RABBITMQ_DEFAULT_USER
    RABBITMQ_DEFAULT_PASS
    RABBITMQ_HOST
    RABBITMQ_PORT

For data base a separate config file `api_db_config.env` is required:

    POSTGRES_DB
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_HOST
    POSTGRES_PORT
