from database import get_connection

connection = get_connection()
cursor = connection.cursor()

# ---------------------------------
# COMPANIES TABLE
# ---------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS scraper_runs (
    id SERIAL PRIMARY KEY,
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