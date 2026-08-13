# ---------------------------------
# CHECK JOB DATABASE
# ---------------------------------


from database import get_connection



connection = get_connection()


cursor = connection.cursor()



cursor.execute(

    """

    SELECT

    company,

    title,
    
    category,

    location,

    remote,

    status,

    url


    FROM jobs


    ORDER BY id DESC


    LIMIT 20


    """

)



jobs = cursor.fetchall()



print(

    "Jobs Found:",

    len(jobs)

)



for job in jobs:


    print("------------------------")


    print(

        dict(job)

    )



connection.close()