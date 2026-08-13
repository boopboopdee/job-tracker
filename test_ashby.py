from automation.parsers.ashby import get_ashby_jobs


company = {

"name":"Nerdwallet",

"board":"nerdwallet"

}


jobs = get_ashby_jobs(company)


print(
    "Jobs found:",
    len(jobs)
)


for job in jobs[:5]:

    print(job)