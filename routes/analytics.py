from flask import Blueprint, render_template, request

from database import get_connection


analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/analytics")
def analytics():

    # ---------------------------------
    # ANALYTICS FILTERS
    # ---------------------------------

    state_filter = request.args.get(
        "state",
        ""
    )

    chart_filter = request.args.get(
        "chart",
        "jobs"
    )

    remote_filter = request.args.get(
        "remote",
        ""
    )

    connection = get_connection()
    cursor = connection.cursor()


    # ---------------------------------
    # JOBS BY COMPANY
    # ---------------------------------

    company_query = """
        SELECT
            company,
            COUNT(*) AS total
        FROM jobs
        WHERE 1=1
    """

    company_params = []

    if state_filter:
        company_query += """
            AND location LIKE %s
        """

        company_params.append(
            f"%{state_filter}%"
        )

    if remote_filter:
        company_query += """
            AND (
                remote = %s
                OR location LIKE '%Remote%'
            )
        """

        company_params.append(
            remote_filter
        )

    company_query += """
        GROUP BY company
        ORDER BY total DESC
        LIMIT 10
    """

    cursor.execute(
        company_query,
        company_params
    )

    companies = [
        {
            "company": row["company"],
            "total": row["total"]
        }
        for row in cursor.fetchall()
    ]


    # ---------------------------------
    # JOB CATEGORIES
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            category,
            COUNT(*) AS total

        FROM jobs

        GROUP BY category

        ORDER BY total DESC
        """
    )

    categories = [
        {
            "category": row["category"],
            "total": row["total"]
        }
        for row in cursor.fetchall()
    ]


    # ---------------------------------
    # STATUS COUNTS
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            status,
            COUNT(*) AS total

        FROM jobs

        GROUP BY status
        """
    )

    counts = {
        "New": 0,
        "Applied": 0,
        "Interviewing": 0,
        "Rejected": 0
    }

    for row in cursor.fetchall():

        status = row["status"]

        if status in counts:
            counts[status] = row["total"]


    # ---------------------------------
    # LOCATION DATA WITH FILTERS
    # ---------------------------------

    location_query = """
        SELECT
            location,
            COUNT(*) AS total

        FROM jobs

        WHERE 1=1
    """

    location_params = []

    if state_filter:

        location_query += """
            AND location LIKE %s
        """

        location_params.append(
            f"%{state_filter}%"
        )

    if remote_filter:

        location_query += """
            AND (
                remote = %s
                OR location LIKE '%Remote%'
            )
        """

        location_params.append(
            remote_filter
        )

    location_query += """
        GROUP BY location

        ORDER BY total DESC

        LIMIT 10
    """

    cursor.execute(
        location_query,
        location_params
    )

    location_counts = {
        row["location"]: row["total"]
        for row in cursor.fetchall()
    }


    # ---------------------------------
    # REMOTE DATA
    # ---------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE remote = 'Remote'
        OR location LIKE '%Remote%'
        """
    )

    remote = cursor.fetchone()["total"]


    # ---------------------------------
    # TOTAL JOBS
    # ---------------------------------

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        """
    )

    total_jobs = cursor.fetchone()["total"]


    # ---------------------------------
    # REMOTE BREAKDOWN
    # ---------------------------------

    remote_breakdown = {

        "Remote": remote,

        "On-site": total_jobs - remote

    }


    # ---------------------------------
    # TREND DATA
    # ---------------------------------

    cursor.execute(
        """
        SELECT
            date_found::date AS date,
            COUNT(*) AS total

        FROM jobs

        WHERE date_found::date >= CURRENT_DATE - INTERVAL '30 days'

        GROUP BY date_found::date

        ORDER BY date_found::date
        """
    )

    trend_data = {
        row["date"]: row["total"]
        for row in cursor.fetchall()
    }


    # ---------------------------------
    # CLOSE DATABASE
    # ---------------------------------

    connection.close()


    # ---------------------------------
    # RENDER ANALYTICS PAGE
    # ---------------------------------

    return render_template(
        "analytics.html",

        companies=companies,

        state_filter=state_filter,

        chart_filter=chart_filter,

        remote_filter=remote_filter,

        remote_breakdown=remote_breakdown,

        categories=categories,

        counts=counts,

        location_counts=location_counts,

        trend_data=trend_data
    )