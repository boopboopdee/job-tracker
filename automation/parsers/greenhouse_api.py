# ---------------------------------
# GREENHOUSE API JOB PARSER
# ---------------------------------


import requests
from automation.parsers.parser_base import normalize_job




# ---------------------------------
# GET JOBS FROM GREENHOUSE API
# ---------------------------------
def detect_remote(location, title):

    text = (
        location + " " + title
    ).lower()


    if "remote" in text:
        return "Remote"

    elif "hybrid" in text:
        return "Hybrid"

    else:
        return "On-site"

def get_greenhouse_api_jobs(company):


    jobs = []

    job_keywords = [

        "marketing analyst",

        "marketing operations",

        "data analyst",

        "business intelligence",

        "revenue operations",

        "growth analyst",

        "crm analyst",

        "customer insights",

        "product marketing",

        "sales operations",

        "business systems",

        "marketing analytics",

        "analytics",

        "account executive",

        "account manager"

    ]

    # ---------------------------------
    # BUILD GREENHOUSE API URL
    # ---------------------------------

    url = (

            "https://boards-api.greenhouse.io/v1/boards/"

            + company["board"]

            + "/jobs"

    )



    response = requests.get(

        url

    )



    data = response.json()



    for job in data.get(

        "jobs",

        []

    ):

        title = job.get(

            "title",

            ""

        )


        if not any(

            keyword in title.lower()

            for keyword in job_keywords

        ):

            continue

        title = job.get(

            "title",

            ""

        )



        job_url = job.get(

            "absolute_url",

            ""

        )



        location = "Unknown"



        remote = "Unknown"



        salary = "Unknown"



        # ---------------------------------
        # LOCATION
        # ---------------------------------


        location_data = job.get(

            "location"

        )


        if location_data:


            location = location_data.get(

                "name",

                "Unknown"

            )



        # ---------------------------------
        # REMOTE CHECK
        # ---------------------------------


        if "remote" in title.lower():

            remote = "Remote"

        jobs.append(

            normalize_job(

                title,

                job_url,

                location,

                detect_remote(
                    location,
                    title
                ),

                salary

            )

        )


    return jobs