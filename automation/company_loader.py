# ---------------------------------
# COMPANY LOADER
# Loads active scraper companies
# ---------------------------------


from database import get_connection




def normalize_parser(value):


    if value == "greenhouse_api":

        return "greenhouse"


    return value




def get_active_companies():


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT *

        FROM companies

        WHERE active = 1
        """
    )



    rows = cursor.fetchall()



    companies = []



    for row in rows:



        parser = normalize_parser(

            row["parser_type"]

        )



        platform = normalize_parser(

            row["platform"]

        )



        if not parser:

            parser = platform



        company = {


            "id":
            row["id"],


            "name":
            row["name"],


            "platform":
            platform,


            "parser_type":
            parser,


            "board":
            row["board"],


            "url":
            row["url"] or ""

        }



        companies.append(
            company
        )



    connection.close()


    return companies