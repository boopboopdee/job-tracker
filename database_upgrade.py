from database import get_connection


connection = get_connection()

cursor = connection.cursor()


columns = [

    """
    ALTER TABLE jobs
    ADD COLUMN experience TEXT
    """,

    """
    ALTER TABLE jobs
    ADD COLUMN department TEXT
    """,

    """
    ALTER TABLE jobs
    ADD COLUMN skills TEXT
    """,

    """
    ALTER TABLE jobs
    ADD COLUMN category TEXT
    """,

    """
    ALTER TABLE companies
    ADD COLUMN parser_type TEXT
    """,

    """
    ALTER TABLE companies
    ADD COLUMN board TEXT
    """

]


for column in columns:

    try:

        cursor.execute(column)

        print(
            "Added column"
        )


    except Exception as error:

        print(
            "Skipped:",
            error
        )



connection.commit()

connection.close()


print(
    "Database upgrade complete."
)