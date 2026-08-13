from flask import Blueprint, redirect

from database import get_connection



status_bp = Blueprint(
    "status",
    __name__
)



# ---------------------------------
# VALID STATUSES
# ---------------------------------

VALID_STATUSES = [

    "New",

    "Applied",

    "Interviewing",

    "Rejected"

]



@status_bp.route(
"/update-status/<int:id>/<status>"
)
def update_status(id,status):
    # ---------------------------------
    # CHECK STATUS
    # ---------------------------------

    if status not in VALID_STATUSES:
        return "Invalid Status"


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """
        UPDATE jobs

        SET status=?

        WHERE id=?

        """,

        (
            status,
            id
        )

    )


    connection.commit()

    connection.close()



    return redirect("/jobs")