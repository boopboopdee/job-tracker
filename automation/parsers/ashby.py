# ---------------------------------
# ASHBY JOB PARSER
# ---------------------------------

import requests


def get_ashby_jobs(company):


    jobs = []


    board = company.get(
        "board"
    )


    if not board:

        return jobs



    url = (
        "https://api.ashbyhq.com/"
        f"posting-api/job-board/{board}"
    )


    print(
        "ASHBY URL:",
        url
    )


    response = requests.get(
        url,
        timeout=20
    )


    if response.status_code != 200:

        print(
            "Ashby failed:",
            response.status_code
        )

        return jobs



    data = response.json()



    for job in data.get("jobs", []):


        jobs.append({

            "company":
            company["name"],


            "title":
            job.get("title",""),


            "location":
            job.get("location",""),


            "url":
            job.get("jobUrl",""),


            "job_source":
            "ashby"

        })


    return jobs