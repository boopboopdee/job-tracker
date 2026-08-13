# ---------------------------------
# ADD COMPANY TO DATABASE
# ---------------------------------

from database import get_connection

from automation.company_analyzer import analyze_company




def add_company(url):


    company = analyze_company(url)



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
        active
        )

        VALUES (?,?,?,?,?)

        """,

        (

        company["name"],

        company["platform"],

        company["board"],

        company["url"],

        company["active"]

        )

    )



    connection.commit()

    connection.close()



    print()

    print("====================")

    print("COMPANY ADDED")

    print("====================")

    print(
        "Name:",
        company["name"]
    )

    print(
        "Platform:",
        company["platform"]
    )

    print(
        "Board:",
        company["board"]
    )
# ---------------------------------
# TEST COMPANY ADDITIONS HERE
# ---------------------------------


if __name__ == "__main__":


    add_company(

        "Netflix",

        "greenhouse",

        "netflix",

        None

    )