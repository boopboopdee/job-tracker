import sqlite3
import psycopg2
import os


# ---------------------------------
# CONNECT TO LOCAL SQLITE DATABASE
# ---------------------------------

sqlite_connection = sqlite3.connect("jobs.db")

sqlite_cursor = sqlite_connection.cursor()

sqlite_cursor.execute("""
    SELECT
        name,
        platform,
        parser_type,
        board,
        url,
        active
    FROM companies
""")

companies = sqlite_cursor.fetchall()

sqlite_connection.close()


print(f"Found {len(companies)} companies in local database.")


# ---------------------------------
# CONNECT TO RENDER POSTGRESQL
# ---------------------------------

database_url = os.environ.get("DATABASE_URL")

if not database_url:
    database_url = input(
        "Paste your Render EXTERNAL DATABASE URL: "
    ).strip()


postgres_connection = psycopg2.connect(
    database_url
)

postgres_cursor = postgres_connection.cursor()


# ---------------------------------
# INSERT COMPANIES
# ---------------------------------

for company in companies:

    name, platform, parser_type, board, url, active = company

    postgres_cursor.execute(
        """
        INSERT INTO companies
        (
            name,
            platform,
            parser_type,
            board,
            url,
            active,
            favorite
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, 0)
        """,
        (
            name,
            platform,
            parser_type,
            board,
            url,
            active
        )
    )


# ---------------------------------
# SAVE
# ---------------------------------

postgres_connection.commit()


print(
    f"Successfully inserted {len(companies)} companies into Render."
)


# ---------------------------------
# CLOSE
# ---------------------------------

postgres_cursor.close()

postgres_connection.close()
