# ---------------------------------
# ADD CATEGORY COLUMN
# ---------------------------------

import sqlite3


connection = sqlite3.connect(
    "jobs.db"
)


cursor = connection.cursor()



cursor.execute(

    """

    ALTER TABLE jobs

    ADD COLUMN category TEXT

    """

)



connection.commit()

connection.close()



print(
    "Category column added"
)