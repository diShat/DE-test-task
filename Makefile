# Load environment variables from .env
include .env

# Variables
DOCKER_COMPOSE = docker-compose
DUMP_FILE = dump.sql

# Run database
up:
	$(DOCKER_COMPOSE) up -d

# Stop database
down:
	$(DOCKER_COMPOSE) down

# Run ETL scripts
extract:
	python src/fetch_api_script.py

transform:
	python src/transform_data_script.py

load:
	python src/load_to_db_script.py

etl: extract transform load

# Run reports
report:
	python src/sql_reports_script.py

dump:
	$(DOCKER_COMPOSE) exec postgres \
		pg_dump -U $(DB_USER) $(DB_NAME) > dump.sql

# Install dependencies
requirements:
	pip install -r requirements.txt