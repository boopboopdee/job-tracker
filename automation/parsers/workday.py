# ---------------------------------
# WORKDAY JOB PARSER
# ---------------------------------

import requests
from urllib.parse import urlparse


# ---------------------------------
# GET JOBS FROM WORKDAY
# ---------------------------------

def get_workday_jobs(company):

    jobs = []

    MAX_JOBS = 1500

    url = company["url"]

    api_url = build_workday_api(url)

    print("Workday API:")
    print(api_url)


    offset = 0

    limit = 20

    seen_jobs = set()

    total_jobs = None


    while True:


        try:

            response = requests.post(

                api_url,

                json={

                    "appliedFacets": {},

                    "limit": limit,

                    "offset": offset,

                    "searchText": ""

                },

                headers={

                    "User-Agent":
                        "Mozilla/5.0",

                    "Accept":
                        "application/json",

                    "Content-Type":
                        "application/json"

                },

                timeout=20

            )


            if response.status_code != 200:

                print(
                    "Workday API failed:",
                    response.status_code
                )

                print(
                    response.text[:500]
                )

                break



            data = response.json()


            if total_jobs is None:

                total_jobs = data.get(
                    "total",
                    0
                )

                print(
                    "Total Workday jobs:",
                    total_jobs
                )



            postings = data.get(
                "jobPostings",
                []
            )


            if not postings:

                print(
                    "No more jobs."
                )

                break



            print(
                "Batch:",
                len(postings),
                "Offset:",
                offset
            )



            for item in postings:


                external_path = item.get(
                    "externalPath",
                    ""
                )


                if not external_path:
                    continue


                if external_path in seen_jobs:
                    continue


                seen_jobs.add(
                    external_path
                )


                title = item.get(
                    "title",
                    ""
                )


                if not title:
                    continue



                location = item.get(
                    "locationsText",
                    "Unknown"
                )



                jobs.append(

                    {

                        "title":
                            title,


                        "url":
                            build_job_url(
                                url,
                                external_path
                            ),


                        "location":
                            location,


                        "remote":
                            detect_remote(
                                title
                                + " "
                                + location
                                + " "
                                + external_path
                            ),


                        "salary":
                            "Unknown"

                    }

                )


                if len(jobs) >= MAX_JOBS:

                    print(
                        "Maximum jobs collected."
                    )

                    return jobs



            offset += limit



            if offset >= total_jobs:

                print(
                    "All Workday jobs collected."
                )

                break



        except Exception as error:


            print(
                "Workday parser error:",
                error
            )

            break



    return jobs

# ---------------------------------
# BUILD API URL
# ---------------------------------

def build_workday_api(url):


    parsed = urlparse(url)


    host = parsed.netloc


    parts = parsed.path.strip("/").split("/")


    tenant = host.split(".")[0]


    site = ""


    if len(parts) >= 2:

        site = parts[1]


    return (

        "https://"
        + host
        + "/wday/cxs/"
        + tenant
        + "/"
        + site
        + "/jobs"

    )



# ---------------------------------
# GET HOST
# ---------------------------------

def get_host(url):


    return urlparse(url).netloc



# ---------------------------------
# REMOTE DETECTOR
# ---------------------------------

def detect_remote(text):

    text = text.lower()


    remote_words = [
        "remote",
        "virtual",
        "work from home",
        "wfh"
    ]


    hybrid_words = [
        "hybrid"
    ]


    for word in remote_words:

        if word in text:
            return "Remote"


    for word in hybrid_words:

        if word in text:
            return "Hybrid"


    return "On-site"

# ---------------------------------
# BUILD JOB APPLICATION URL
# ---------------------------------

def build_job_url(
        career_url,
        external_path
):


    if not external_path:
        return ""



    # Already complete URL
    if external_path.startswith(
        "http"
    ):
        return external_path



    parsed = urlparse(
        career_url
    )


    base = (
        parsed.scheme
        + "://"
        + parsed.netloc
    )


    return (
        base
        +
        external_path
    )