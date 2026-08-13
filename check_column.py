import sqlite3


connection = sqlite3.connect(
    "jobs.db"
)


cursor = connection.cursor()



cursor.execute(
    "PRAGMA table_info(jobs)"
)


for column in cursor.fetchall():

    print(column)



connection.close()