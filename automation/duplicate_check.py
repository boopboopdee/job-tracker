# ---------------------------------
# DUPLICATE JOB CHECK
# ---------------------------------


from database import get_connection



# ---------------------------------
# CHECK IF JOB EXISTS
# ---------------------------------

def job_exists(
    url,
    title,
    company
):


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT id

        FROM jobs

        WHERE

        url = ?

        OR

        (
            title = ?

            AND

            company = ?

        )

        """,

        (

            url,

            title,

            company

        )

    )



    result = cursor.fetchone()



    connection.close()



    return result is not None