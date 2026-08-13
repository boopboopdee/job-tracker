# ---------------------------------
# TEST GREENHOUSE RESULTS
# ---------------------------------


from automation.parsers.greenhouse import get_greenhouse_jobs



jobs = get_greenhouse_jobs(

    "https://www.hubspot.com/careers"

)



print(

    "Number of jobs found:",

    len(jobs)

)



for job in jobs[:10]:


    print(job)