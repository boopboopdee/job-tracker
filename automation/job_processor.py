def process_jobs(company, jobs):

    saved = []

    for job in jobs:

        if not is_valid_job(job["title"]):
            continue

        if not matches_keyword(job["title"]):
            continue


        save_job(
            company["name"],
            job["title"],
            job["url"],
            job.get("location"),
            job.get("remote"),
            job.get("salary")
        )


        saved.append(job)


    return saved