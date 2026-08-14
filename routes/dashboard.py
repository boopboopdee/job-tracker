from flask import Blueprint, render_template, Response, stream_with_context, redirect
import json

from database import get_connection
from automation.scraper import run_scraper

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------
    # JOB STATUS COUNTS
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            status,
            COUNT(*) as total
        FROM jobs
        GROUP BY status
        """
    )

    status_results = cursor.fetchall()

    counts = {
        "New": 0,
        "Applied": 0,
        "Interviewing": 0,
        "Rejected": 0
    }

    for row in status_results:
        if row["status"] in counts:
            counts[row["status"]] = row["total"]

    # ---------------------------------
    # JOBS BY COMPANY
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            company,
            COUNT(*) as total
        FROM jobs
        GROUP BY company
        ORDER BY total DESC
        """
    )

    company_rows = cursor.fetchall()

    company_results = [
        {
            "company": row["company"],
            "total": row["total"]
        }
        for row in company_rows
    ]

    # ---------------------------------
    # JOBS BY CATEGORY
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            category,
            COUNT(*) as total
        FROM jobs
        GROUP BY category
        ORDER BY total DESC
        """
    )

    category_rows = cursor.fetchall()

    category_results = [
        {
            "category": row["category"],
            "total": row["total"]
        }
        for row in category_rows
    ]

    # ---------------------------------
    # TOTAL JOB COUNT
    # ---------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM jobs
        """
    )

    total_jobs = cursor.fetchone()["total"]

    # ---------------------------------
    # JOBS BY LOCATION
    # ---------------------------------

    # Las Vegas
    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM jobs
        WHERE location LIKE '%Las Vegas%'
        """
    )

    location_counts = {
        "Las Vegas": cursor.fetchone()["total"]
    }

    # Henderson
    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM jobs
        WHERE location LIKE '%Henderson%'
        """
    )

    location_counts["Henderson"] = cursor.fetchone()["total"]

    # Nevada
    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM jobs
        WHERE location LIKE '%Nevada%'
           OR location LIKE '%Las Vegas%'
           OR location LIKE '%Henderson%'
        """
    )

    location_counts["Nevada"] = cursor.fetchone()["total"]

    # West Coast
    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM jobs
        WHERE location LIKE '%California%'
           OR location LIKE '%Oregon%'
           OR location LIKE '%Washington%'
           OR location LIKE '%Nevada%'
           OR location LIKE '%Remote%'
        """
    )

    location_counts["West Coast"] = cursor.fetchone()["total"]

    # Remote
    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM jobs
        WHERE remote = 'Remote'
           OR location LIKE '%Remote%'
        """
    )

    location_counts["Remote"] = cursor.fetchone()["total"]

    # ---------------------------------
    # REMOTE BREAKDOWN
    # ---------------------------------

    remote_count = location_counts["Remote"]

    onsite_count = total_jobs - remote_count

    remote_breakdown = {
        "Remote": remote_count,
        "On-site": onsite_count
    }

    # ---------------------------------
    # JOBS FOUND TREND
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            date_found::date AS date,
            COUNT(*) AS total
        FROM jobs
        WHERE date_found::date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY date_found::date
        ORDER BY date_found::date ASC
        """
    )

    trend_results = cursor.fetchall()

    trend_data = {
        str(row["date"]): row["total"]
        for row in trend_results
    }

    # ---------------------------------
    # JOBS ADDED TODAY
    # ---------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE date_found::date = CURRENT_DATE
        """
    )

    row = cursor.fetchone()
    jobs_today = row["total"] if row else 0

    connection.close()

    return render_template(
        "index.html",
        counts=counts,
        companies=company_results,
        categories=category_results,
        total_jobs=total_jobs,
        jobs_today=jobs_today,
        location_counts=location_counts,
        remote_breakdown=remote_breakdown,
        trend_data=trend_data
    )


# ---------------------------------
# LIVE JOB SEARCH WITH PROGRESS
# ---------------------------------

@dashboard_bp.route("/search-live")
def search_live():

    def generate():

        for update in run_scraper():

            yield f"data: {json.dumps(update)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream"
    )


# ---------------------------------
# REFRESH DASHBOARD
# ---------------------------------

@dashboard_bp.route("/refresh-dashboard")
def refresh_dashboard():

    return redirect("/")