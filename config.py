import os

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret-key"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "jobs.db"
)

DEBUG = os.getenv(
    "FLASK_DEBUG",
    "False"
).lower() == "true"

ADMIN_KEY = os.getenv(
    "ADMIN_KEY"
)