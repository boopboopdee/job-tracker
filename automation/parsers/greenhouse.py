import requests



def get_greenhouse_jobs(company):


    board = company.get(
        "board"
    )


    if not board:

        return []



    url = (
        f"https://boards-api.greenhouse.io/v1/"
        f"boards/{board}/jobs"
    )


    response = requests.get(
        url,
        timeout=15
    )


    data = response.json()


    jobs=[]



    keywords=[

        "analyst",
        "marketing",
        "account executive",
        "account manager",
        "operations",
        "business intelligence",
        "revenue",
        "crm",
        "growth"

    ]



    for job in data.get(
        "jobs",
        []
    ):


        title = job["title"]


        if not any(
            word in title.lower()
            for word in keywords
        ):

            continue



        jobs.append({

            "title":
                title,


            "url":
                job["absolute_url"],


            "location":
                job.get(
                    "location",
                    {}
                ).get(
                    "name",
                    "Unknown"
                ),


            "remote":
                "Unknown",


            "salary":
                "Unknown"

        })


    return jobs