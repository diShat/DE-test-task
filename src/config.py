import os
from dotenv import load_dotenv

# Load .env
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# API
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")  # Will be None for this API
API_HEADERS = {"accept": "application/json"}

# Data storage
DATA_RAW_PATH = os.path.join(PROJECT_ROOT, os.getenv("DATA_RAW_PATH"))
DATA_PROCESSED_PATH = os.path.join(PROJECT_ROOT, os.getenv("DATA_PROCESSED_PATH"))

# Postgres
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")