KEYWORDS = [

    "analyst",

    "data",

    "analytics",

    "business intelligence",

    "revenue operations",

    "sales operations",

    "marketing",

    "crm",

    "account executive",

    "account manager",

    "customer success"

]



BAD_WORDS = [

    "intern",

    "warehouse",

    "driver",

    "maintenance",

    "security"

]



def score_job(job):


    title = job.get(
        "title",
        ""
    ).lower()


    score = 0



    for word in KEYWORDS:

        if word in title:

            score += 10



    for word in BAD_WORDS:

        if word in title:

            score -= 20



    return score



def keep_job(job):


    return score_job(job) >= 10