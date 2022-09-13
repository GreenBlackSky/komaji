#!/bin/bash

python app/utils/check_db_connection.py
cd app
alembic upgrade head
cd -
uvicorn app.main:app --reload --host 0.0.0.0