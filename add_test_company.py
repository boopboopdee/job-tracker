from database import get_connection


connection = get_connection()

cursor = connection.cursor()


cursor.execute(
    """
    INSERT INTO companies
    (
        name,
        platform,
        board,
        url
    )

    VALUES (?,?,?,?)

    """,

    (
        "HubSpot",
        "greenhouse_api",
        "hubspot",
        None
    )

)


connection.commit()

connection.close()


print("Company added!")