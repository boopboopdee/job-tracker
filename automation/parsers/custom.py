# ---------------------------------
# CUSTOM JOB PARSER
# ---------------------------------

import requests

from bs4 import BeautifulSoup



# ---------------------------------
# GET JOBS FROM CUSTOM CAREER PAGE
# ---------------------------------

def get_custom_jobs(company):


    jobs = []


    url = company["url"]


    response = requests.get(

        url,

        timeout=10

    )


    soup = BeautifulSoup(

        response.text,

        "html.parser"

    )



    # ---------------------------------
    # FIND LINKS
    # ---------------------------------

    for link in soup.find_all(

        "a",

        href=True

    ):


        title = link.text.strip()


        job_url = link["href"]



        if title:


            if job_url.startswith("/"):

                job_url = url + job_url



            jobs.append(

                {

                "title": title,

                "url": job_url,

                "location": "Unknown",

                "remote": "Unknown",

                "salary": "Unknown"

                }

            )


    return jobs