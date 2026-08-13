# ---------------------------------
# LEVER JOB PARSER
# ---------------------------------

import requests



# ---------------------------------
# GET LEVER JOBS
# ---------------------------------

def get_lever_jobs(company):


    jobs = []


    url = (

        "https://api.lever.co/v0/postings/"

        + company["board"]

    )



    response = requests.get(

        url

    )



    data = response.json()



    for job in data:



        jobs.append(

            {

                "title":
                job.get(
                    "text",
                    ""
                ),


                "url":
                job.get(
                    "hostedUrl",
                    ""
                ),


                "location":
                job.get(
                    "categories",
                    {}
                ).get(
                    "location",
                    "Unknown"
                ),


                "remote":
                "Unknown",


                "salary":
                "Unknown"

            }

        )



    return jobs