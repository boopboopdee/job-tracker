from automation.parsers.greenhouse_api import get_greenhouse_api_jobs



jobs = get_greenhouse_api_jobs(

    "airbnb"

)



print(

    "Jobs found:",

    len(jobs)

)



for job in jobs[:10]:

    print(job)