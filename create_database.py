import sqlite3


connection = sqlite3.connect("jobs.db")

cursor = connection.cursor()


# ---------------------------------
# JOBS TABLE
# ---------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company TEXT NOT NULL,

    title TEXT NOT NULL,

    location TEXT,

    remote TEXT,

    salary TEXT,

    url TEXT UNIQUE,

    date_found TEXT,

    status TEXT DEFAULT 'New',

    notes TEXT,

    date_applied TEXT,

    favorite INTEGER DEFAULT 0,

    job_source TEXT,

    category TEXT

)
""")


# ---------------------------------
# SCRAPER HISTORY TABLE
# ---------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS scraper_runs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    run_date TEXT,

    companies_checked INTEGER,

    jobs_found INTEGER,

    jobs_added INTEGER,

    duplicates INTEGER

)
""")


## ---------------------------------
# COMPANIES TABLE
# ---------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS companies(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    platform TEXT,

    board TEXT,

    url TEXT,

    active INTEGER DEFAULT 1

)

""")

# ---------------------------------
# SAVE CHANGES
# ---------------------------------

connection.commit()


connection.close()


print("Database created!")