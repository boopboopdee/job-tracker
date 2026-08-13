import sqlite3


connection = sqlite3.connect("jobs.db")

cursor = connection.cursor()


# ---------------------------------
# SHOW ALL TABLES
# ---------------------------------

cursor.execute(
    """
    SELECT name

    FROM sqlite_master

    WHERE type='table'
    """
)


tables = cursor.fetchall()


print("Tables Found:")

for table in tables:

    print(table[0])


# ---------------------------------
# SHOW COMPANIES COLUMNS
# ---------------------------------

print("\nCompanies Table:")

cursor.execute(
    """
    PRAGMA table_info(companies)
    """
)


for row in cursor.fetchall():

    print(row)


# ---------------------------------
# SHOW SCRAPER HISTORY COLUMNS
# ---------------------------------

print("\nScraper Runs Table:")

cursor.execute(
    """
    PRAGMA table_info(scraper_runs)
    """
)


for row in cursor.fetchall():

    print(row)



connection.close()