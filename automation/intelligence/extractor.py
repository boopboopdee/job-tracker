import re



def extract_remote(job):


    text = (
        job.get("title","")
        +
        job.get("location","")
        +
        job.get("description","")
    ).lower()



    if "remote" in text:

        return True


    return False




def extract_experience(job):


    text = job.get(
        "description",
        ""
    ).lower()



    numbers = re.findall(
        r"\d+\+?\s+years",
        text
    )


    if numbers:

        return numbers[0]


    return None

import re



def extract_experience(text):

    text=text.lower()


    patterns=[

        r"(\d+)\+?\s+years",

        r"(\d+)-(\d+)\s+years"

    ]


    for pattern in patterns:

        match=re.search(
            pattern,
            text
        )

        if match:

            return match.group()


    return "Unknown"




def extract_salary(text):


    matches=re.findall(

        r"\$[\d,]+",

        text

    )


    if matches:

        return matches[0]


    return "Unknown"




def extract_remote(text):


    text=text.lower()


    if "remote" in text:

        return "Remote"


    if "hybrid" in text:

        return "Hybrid"


    return "Onsite"

# ---------------------------------
# SKILL EXTRACTION
# ---------------------------------

def extract_skills(text):

    skills = [

        "python",
        "sql",
        "tableau",
        "power bi",
        "excel",
        "salesforce",
        "hubspot",
        "crm",
        "google analytics",
        "aws",
        "snowflake"

    ]


    found = []


    text = text.lower()


    for skill in skills:

        if skill in text:

            found.append(skill)


    if found:

        return ", ".join(found)


    return "Unknown"



# ---------------------------------
# DEPARTMENT CLASSIFIER
# ---------------------------------

def classify_department(text):

    text = text.lower()


    departments = {


        "Marketing":
        [
            "marketing",
            "growth",
            "campaign",
            "seo"
        ],


        "Sales":
        [
            "sales",
            "account executive",
            "business development"
        ],


        "Analytics":
        [
            "analyst",
            "analytics",
            "business intelligence",
            "data"
        ],


        "Operations":
        [
            "operations",
            "revenue operations",
            "sales operations"
        ]

    }


    for department, keywords in departments.items():

        for keyword in keywords:

            if keyword in text:

                return department


    return "Unknown"

# ---------------------------------
# SALARY EXTRACTION
# ---------------------------------

import re


def extract_salary(text):

    matches = re.findall(
        r"\$[\d,]+",
        text
    )


    if matches:

        return matches[0]


    return "Unknown"