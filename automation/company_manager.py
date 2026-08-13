# ---------------------------------
# COMPANY DATABASE MANAGER
# ---------------------------------

from database import get_connection

from automation.company_detector import (
    detect_company_platform,
    extract_company_name,
    extract_board
)




# ---------------------------------
# ADD COMPANY FROM URL
# ---------------------------------

def add_company_from_url(url):


    info = detect_company_platform(url)



    name = extract_company_name(url)



    board = extract_board(url)



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """
        INSERT INTO companies
        (
        name,
        platform,
        board,
        url,
        active,
        parser_type
        )

        VALUES (?,?,?,?,?,?)

        """,

        (

        name,

        info["platform"],

        board,

        url,

        1,

        info["parser_type"]

        )

    )



    connection.commit()

    connection.close()



    return {

        "name":name,

        "platform":info["platform"],

        "board":board

    }