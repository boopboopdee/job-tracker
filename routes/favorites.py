from flask import Blueprint, redirect

from database import get_connection



favorites_bp = Blueprint(

    "favorites",

    __name__

)



# ---------------------------------
# TOGGLE FAVORITE
# ---------------------------------

@favorites_bp.route(
"/favorite/<int:id>"
)

def favorite(id):


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

    """

    UPDATE jobs

    SET favorite =

    CASE

    WHEN favorite = 1 THEN 0

    ELSE 1

    END


    WHERE id=%s

    """,

    (id,)

    )


    connection.commit()

    connection.close()


    return redirect("/jobs")