from flask import Blueprint, render_template

from database import get_connection


applications_bp = Blueprint(
    "applications",
    __name__
)


def get_jobs_by_status(status):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM jobs

        WHERE status=%s

        ORDER BY company
        """,

        (status,)
    )


    jobs = cursor.fetchall()


    connection.close()


    return jobs



@applications_bp.route("/new-jobs")
def new_jobs():

    jobs = get_jobs_by_status("New")

    return render_template(
        "status_jobs.html",
        jobs=jobs,
        page_title="New Jobs"
    )



@applications_bp.route("/saved-jobs")
def saved_jobs():

    jobs = get_jobs_by_status("Saved")

    return render_template(
        "status_jobs.html",
        jobs=jobs,
        page_title="Saved Jobs"
    )



@applications_bp.route("/applied-jobs")
def applied_jobs():

    jobs = get_jobs_by_status("Applied")

    return render_template(
        "status_jobs.html",
        jobs=jobs,
        page_title="Applied Jobs"
    )



@applications_bp.route("/interviews")
def interviews():

    jobs = get_jobs_by_status("Interview")

    return render_template(
        "status_jobs.html",
        jobs=jobs,
        page_title="Interviews"
    )



@applications_bp.route("/offers")
def offers():

    jobs = get_jobs_by_status("Offer")

    return render_template(
        "status_jobs.html",
        jobs=jobs,
        page_title="Offers"
    )



@applications_bp.route("/rejected")
def rejected():

    jobs = get_jobs_by_status("Rejected")

    return render_template(
        "status_jobs.html",
        jobs=jobs,
        page_title="Rejected Jobs"
    )