from database import get_connection

from automation.intelligence.ats_detector import detect_ats



def repair_companies():


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT *

        FROM companies

        WHERE parser_type IS NULL

        """
    )


    companies = cursor.fetchall()



    for company in companies:


        print(
            "Checking:",
            company["name"]
        )


        ats = detect_ats(
            company["url"]
        )


        cursor.execute(
            """
            UPDATE companies

            SET

            platform=%s,

            parser_type=%s,

            board=%s


            WHERE id=%s

            """,

            (

            ats["platform"],

            ats["parser_type"],

            ats.get("board"),

            company["id"]

            )

        )


    connection.commit()

    connection.close()