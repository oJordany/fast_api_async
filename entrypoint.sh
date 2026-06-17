#!/bin/sh

#executa as migrations do banco de dados
poetry run alembic upgrade head

#inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero_async.app:app