from database import get_connection
from config import DATABASE_URL


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------
    # DATABASE TYPE
    # ---------------------------------

    is_sqlite = DATABASE_URL.endswith(".db")

    if is_sqlite:

        primary_key = "INTEGER PRIMARY KEY AUTOINCREMENT"

    else:

        primary_key = "SERIAL PRIMARY KEY"

    # ---------------------------------
    # COMPANIES TABLE
    # ---------------------------------

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS companies (

        id {primary_key},

        name TEXT NOT NULL,

        platform TEXT,

        parser_type TEXT,

        board TEXT,

        url TEXT,

        active INTEGER DEFAULT 1,

        favorite INTEGER DEFAULT 0

    )
    """)

    # ---------------------------------
    # JOBS TABLE
    # ---------------------------------

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS jobs (

        id {primary_key},

        company TEXT,

        title TEXT,

        location TEXT,

        remote TEXT,

        salary TEXT,

        experience TEXT,

        department TEXT,

        skills TEXT,

        category TEXT,

        url TEXT,

        date_found TEXT,

        status TEXT DEFAULT 'New',

        favorite INTEGER DEFAULT 0,

        job_source TEXT

    )
    """)

    # ---------------------------------
    # SCRAPER HISTORY
    # ---------------------------------

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS scraper_runs (

        id {primary_key},

        run_date TEXT,

        companies_checked INTEGER,

        jobs_found INTEGER,

        matching INTEGER,

        jobs_added INTEGER,

        duplicates INTEGER

    )
    """)

    connection.commit()

    connection.close()

    print("Database tables created.")


if __name__ == "__main__":

    initialize_database()