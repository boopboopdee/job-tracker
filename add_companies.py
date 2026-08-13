from database import get_connection



companies = [

    (
        "AirBnb",
        "greenhouse_api",
        "airbnb",
        None
    ),


    (
        "DoorDash",
        "greenhouse_api",
        "doordashusa",
        None
    ),


    (
        "Salesforce",
        "workday",
        None,
        "https://careers.salesforce.com"
    ),


    (
        "Adobe",
        "custom",
        None,
        "https://careers.adobe.com"
    )

]



connection = get_connection()

cursor = connection.cursor()



for company in companies:


    cursor.execute(

        """
        INSERT INTO companies

        (
        name,
        platform,
        board,
        url
        )

        VALUES (?,?,?,?)

        """,

        company

    )



connection.commit()

connection.close()



print("Companies added!")