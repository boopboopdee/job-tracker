from database import get_connection


connection = get_connection()

cursor = connection.cursor()


cursor.execute(
"""
SELECT *
FROM companies
WHERE name LIKE '%Nerd%'
"""
)


rows = cursor.fetchall()


for row in rows:
    print(dict(row))


connection.close()