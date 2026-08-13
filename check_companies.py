# ---------------------------------
# CHECK COMPANIES
# ---------------------------------

from database import get_connection


connection = get_connection()

cursor = connection.cursor()


cursor.execute(
    """
    SELECT *

    FROM companies

    """
)


companies = cursor.fetchall()


for company in companies:


    print(
        company["id"],
        company["name"],
        company["url"],
        company["platform"]
    )


connection.close()