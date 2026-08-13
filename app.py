# ---------------------------------
# IMPORTS
# ---------------------------------

from flask import Flask

from dotenv import load_dotenv

import config

from routes.companies import companies_bp
from routes.analytics import analytics_bp
from routes.dashboard import dashboard_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.status import status_bp
from routes.favorites import favorites_bp
from routes.admin import admin_bp
from routes.scraper import scraper_bp


# ---------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------

load_dotenv()


# ---------------------------------
# CREATE APPLICATION
# ---------------------------------

app = Flask(__name__)

app.secret_key = config.SECRET_KEY


# ---------------------------------
# REGISTER ROUTES
# ---------------------------------

app.register_blueprint(
    dashboard_bp
)

app.register_blueprint(
    jobs_bp
)

app.register_blueprint(
    applications_bp
)

app.register_blueprint(
    status_bp
)

app.register_blueprint(
    favorites_bp
)

app.register_blueprint(
    admin_bp
)

app.register_blueprint(
    scraper_bp
)

app.register_blueprint(
    companies_bp
)

app.register_blueprint(
    analytics_bp
)


# ---------------------------------
# RUN APPLICATION
# ---------------------------------

if __name__ == "__main__":

    app.run(
        debug=config.DEBUG
    )