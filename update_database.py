import sqlite3



# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

connection = sqlite3.connect(
    "jobs.db"
)

cursor = connection.cursor()



# ---------------------------------
# CHECK IF COLUMN EXISTS
# ---------------------------------

def add_column(column_name, data_type):


    cursor.execute(
        """

        PRAGMA table_info(jobs)

        """
    )


    columns = [

        column[1]

        for column in cursor.fetchall()

    ]


    if column_name not in columns:


        cursor.execute(

            f"""

            ALTER TABLE jobs

            ADD COLUMN {column_name} {data_type}

            """

        )


        print(
            f"{column_name} added"
        )


    else:


        print(
            f"{column_name} already exists"
        )




# ---------------------------------
# ADD NEW COLUMNS
# ---------------------------------


add_column(
    "date_found",
    "TEXT"
)


add_column(
    "date_applied",
    "TEXT"
)


add_column(
    "favorite",
    "INTEGER DEFAULT 0"
)


add_column(
    "job_source",
    "TEXT"
)



# ---------------------------------
# SAVE CHANGES
# ---------------------------------

connection.commit()

connection.close()


print(
    "Database update complete"
)