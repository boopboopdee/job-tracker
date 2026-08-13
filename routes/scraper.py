from flask import (
    Blueprint,
    render_template,
    request,
    abort
)

import config

from automation.scraper import run_scraper

from database import get_connection


scraper_bp = Blueprint(
    "scraper",
    __name__
)


# ---------------------------------
# SEARCH JOBS PAGE
# ---------------------------------

@scraper_bp.route("/search-jobs")
def search_jobs():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        ORDER BY date_found DESC
        LIMIT 100
        """
    )

    jobs = cursor.fetchall()

    connection.close()

    return render_template(
        "scraper_results.html",
        jobs=jobs
    )


# ---------------------------------
# UPDATE JOBS
# ---------------------------------

@scraper_bp.route("/update-jobs")
def update_jobs():

    admin_key = request.args.get("key")

    if not config.ADMIN_KEY or admin_key != config.ADMIN_KEY:
        abort(403)

    final_result = None

    for update in run_scraper():

        if update["type"] == "complete":

            final_result = update["result"]

    return render_template(
        "scraper_results.html",
        result=final_result,
        jobs=(
            final_result["new_job_details"]
            if final_result
            else []
        )
    )