# ---------------------------------
# DATABASE UPGRADE
# ADD MISSING PARSER TYPES
# ---------------------------------


from database import get_connection



connection = get_connection()

cursor = connection.cursor()



# ---------------------------------
# GREENHOUSE
# ---------------------------------

cursor.execute(
    """
    UPDATE companies

    SET parser_type='greenhouse'

    WHERE platform='greenhouse'
    OR platform='greenhouse_api'
    """
)



# ---------------------------------
# WORKDAY
# ---------------------------------

cursor.execute(
    """
    UPDATE companies

    SET parser_type='workday'

    WHERE platform='workday'
    """
)



# ---------------------------------
# CUSTOM
# ---------------------------------

cursor.execute(
    """
    UPDATE companies

    SET parser_type='custom'

    WHERE platform='custom'
    """
)



# ---------------------------------
# LEVER
# ---------------------------------

cursor.execute(
    """
    UPDATE companies

    SET parser_type='lever'

    WHERE platform='lever'
    """
)



connection.commit()

connection.close()



print("Database parser types updated!")