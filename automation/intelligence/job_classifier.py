CATEGORIES = {


"Data Analytics":[

"data analyst",
"analytics",
"business intelligence",
"sql",
"reporting"

],


"Marketing":[

"marketing analyst",
"marketing operations",
"growth",
"campaign",
"crm"

],


"Sales":[

"account executive",
"account manager",
"sales development",
"business development"

],


"Operations":[

"operations",
"revenue operations",
"sales operations"

]

}



def classify_job(title):


    title = title.lower()


    scores = {}


    for category, words in CATEGORIES.items():

        score = 0


        for word in words:

            if word in title:

                score += 1


        scores[category] = score



    best = max(
        scores,
        key=scores.get
    )


    if scores[best] == 0:

        return "Other"


    return best