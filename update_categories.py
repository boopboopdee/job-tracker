# ---------------------------------
# UPDATE EXISTING JOB CATEGORIES
# ---------------------------------


from database import get_connection

from automation.category import get_category



connection = get_connection()

cursor = connection.cursor()



cursor.execute(

    """

    SELECT id, title

    FROM jobs

    WHERE category IS NULL

    """

)



jobs = cursor.fetchall()



print(
    "Jobs needing categories:",
    len(jobs)
)



for job in jobs:


    category = get_category(

        job["title"]

    )


    cursor.execute(

        """

        UPDATE jobs

        SET category = ?

        WHERE id = ?

        """,

        (

        category,

        job["id"]

        )

    )


connection.commit()

connection.close()



print(
    "Categories updated"
)