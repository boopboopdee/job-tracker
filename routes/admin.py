from flask import Blueprint, redirect, render_template

import subprocess


admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route("/run-scraper")
def run_scraper():

    subprocess.run(
        [
            "python",
            "automation/scraper.py"
        ]
    )

    return redirect("/")