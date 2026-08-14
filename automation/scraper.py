# ---------------------------------
# JOB SCRAPER
# ---------------------------------

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import traceback


from automation.company_loader import get_active_companies
from automation.companies import JOB_KEYWORDS
from automation.parser_router import get_jobs
from automation.duplicate_check import job_exists

from automation.intelligence.job_classifier import classify_job
from automation.intelligence.extractor import (
    extract_remote,
    extract_experience,
    extract_skills,
    classify_department
)

from automation.intelligence.ats_detector import detect_ats
from automation.intelligence.salary_detector import extract_salary


from database import get_connection





# ---------------------------------
# BAD TITLES / WEBSITE TEXT
# ---------------------------------

BAD_KEYWORDS = [

    "privacy",
    "terms",
    "cookie",
    "login",
    "sign in",
    "subscribe",
    "newsletter",
    "press release",
    "investor relations",
    "contact us",
    "about us"

]



# ---------------------------------
# VALID JOB CHECK
# Removes website junk only
# Keyword matching decides relevance
# ---------------------------------

def is_valid_job(title):


    if not title:

        return False



    title_lower = title.lower()



    for word in BAD_KEYWORDS:

        if word in title_lower:

            return False



    return True





# ---------------------------------
# KEYWORD MATCHING
# ---------------------------------

def matches_keyword(text):


    if not text:

        return False



    text = text.lower()



    ignored = [

        "you + agents",

        "customer success."

    ]



    for item in ignored:

        if item in text:

            return False



    for keyword in JOB_KEYWORDS:

        if keyword.lower() in text:

            return True



    return False

# ---------------------------------
# LOCATION FILTER BEFORE DATABASE SAVE
# ONLY KEEP DESIRED AREAS
# ---------------------------------

def matches_location(job):
    location = (
        job.get("location", "")
        or
        job.get("locations", "")
        or
        ""
    ).lower()

    description = (
        job.get("description", "")
        or
        ""
    ).lower()


    remote_text = (
        location
        +
        " "
        +
        description
    )


    allowed_locations = [

        # Las Vegas area
        "las vegas",
        "henderson",
        "north las vegas",

        # Nevada
        "nevada",
        "nv",

        # West Coast
        "california",
        "oregon",
        "washington",
        "san francisco",
        "los angeles",
        "tempe",
        "ca",
        "sf",
        "la",

        # Remote
        "remote",
        "united states",
        "usa",
        "us",
        "u.s."

    ]


    for item in allowed_locations:

        if item in remote_text:

            return True


    return False

# ---------------------------------
# GET COMPANY JOBS
# Uses database ATS settings
# Keeps greenhouse_api separate
# ---------------------------------

def scrape_company(company):


    # ---------------------------------
    # COPY COMPANY
    # Prevent thread conflicts
    # ---------------------------------

    company = company.copy()



    # ---------------------------------
    # IF DATABASE DOES NOT HAVE ATS
    # TRY DETECTION
    # ---------------------------------

    if not company.get("parser_type"):


        if company.get("url"):


            ats = detect_ats(
                company["url"]
            )


            company.update(
                ats
            )


        else:


            print(
                "No ATS information:",
                company["name"]
            )


            return []



    print(
        "Using parser:",
        company.get("parser_type")
    )



    # ---------------------------------
    # SEND TO PARSER ROUTER
    #
    # greenhouse_api
    # stays greenhouse_api
    #
    # greenhouse
    # stays greenhouse
    # ---------------------------------

    return get_jobs(company)




# ---------------------------------
# SAVE JOB
# ---------------------------------

def save_job(
        company,
        title,
        url,
        location="Unknown",
        remote="Unknown",
        salary="Unknown",
        experience="Unknown",
        category="Unknown",
        department="Unknown",
        skills="Unknown"
):


    if job_exists(
        url,
        title,
        company
    ):

        return False



    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO jobs
        (
            company,
            title,
            location,
            remote,
            salary,
            experience,
            department,
            skills,
            url,
            date_found,
            status,
            favorite,
            job_source,
            category
        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,?,?)

        """,

        (

            company,
            title,
            location,
            remote,
            salary,
            experience,
            department,
            skills,
            url,
            str(datetime.today().date()),
            "New",
            0,
            company + " Careers",
            category

        )

    )


    conn.commit()

    conn.close()


    print(
        "Added:",
        title
    )


    return True





# ---------------------------------
# PROCESS COMPANY JOBS
# ---------------------------------

def process_company(company):



    stats = {

        "checked": 1,
        "found": 0,
        "matching": 0,
        "saved": 0,
        "new_jobs": []

    }



    print(
        "\nChecking:",
        company["name"]
    )


    try:

        jobs = scrape_company(company)


        stats["found"] = len(jobs)



        for job in jobs:


            title = job.get(
                "title",
                ""
            )


            description = job.get(
                "description",
                ""
            )


            text = (
                title
                +
                " "
                +
                description
            )

            if not is_valid_job(title):
                print(
                    "BAD TITLE FILTER:",
                    company["name"],
                    title
                )

                continue

            if not matches_keyword(text):
                print(
                    "FILTERED OUT:",
                    company["name"],
                    title
                )

                continue

            # ---------------------------------
            # LOCATION FILTER
            # BLOCK JOBS OUTSIDE TARGET AREA
            # ---------------------------------

            if not matches_location(job):
                print(
                    "LOCATION FILTERED:",
                    company["name"],
                    title,
                    job.get("location")
                )

                continue



            stats["matching"] += 1



            remote = extract_remote(text)

            experience = extract_experience(text)

            salary = extract_salary(text)

            category = classify_job(text)

            department = classify_department(text)

            skills = extract_skills(text)



            saved = save_job(

                company["name"],

                title,

                job.get(
                    "url",
                    ""
                ),

                job.get(
                    "location",
                    job.get(
                        "locations",
                        "Unknown"
                    )
                ),

                remote,

                salary,

                experience,

                category,

                department,

                skills

            )



            if saved:

                stats["saved"] += 1

                stats["new_jobs"].append(job)




    except Exception as e:

        print(

            "FAILED:",

            company["name"],

            e

        )

        traceback.print_exc()



    return stats




# ---------------------------------
# SAVE SCRAPER HISTORY
# ---------------------------------

def save_scraper_run(result):


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(

        """
        INSERT INTO scraper_runs
        (
            run_date,
            companies_checked,
            jobs_found,
            matching,
            jobs_added,
            duplicates
        )

        VALUES (?,?,?,?,?,?)

        """,

        (

            str(datetime.today().date()),

            result["companies"],

            result["found"],

            result["matching"],

            result["added"],

            result["duplicates"]

        )

    )


    conn.commit()

    conn.close()



# ---------------------------------
# RUN SCRAPER
# ---------------------------------

def run_scraper():


    companies = get_active_companies()



    total = {

        "companies":0,
        "found":0,
        "matching":0,
        "added":0,
        "duplicates":0,
        "new_job_details":[]

    }



    print(
        "\nSTARTING SCRAPER:",
        len(companies),
        "companies"
    )



    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:



        futures = {

            executor.submit(
                process_company,
                company
            ): company

            for company in companies

        }



        for future in as_completed(futures):


            company = futures[future]


            result = future.result()



            total["companies"] += result["checked"]

            total["found"] += result["found"]

            total["matching"] += result["matching"]

            total["added"] += result["saved"]

            total["new_job_details"].extend(
                result["new_jobs"]
            )

            yield {

                "type": "progress",

                "company": company["name"],

                "found": result["found"],

                "matching": result["matching"],

                "saved": result["saved"],

                # ---------------------------------
                # LIVE DASHBOARD COUNTERS
                # ---------------------------------

                "current": total["companies"],

                "total": len(companies),

                "added": total["added"],

                "jobs": total["new_job_details"]

            }

    total["duplicates"] = 0



    print(
        "\nSCRAPER COMPLETE"
    )


    yield {

        "type":"complete",

        "result":total

    }




# ---------------------------------
# COMMAND LINE TEST
# ---------------------------------

if __name__ == "__main__":


    final = None


    for update in run_scraper():

        if update["type"] == "complete":

            final = update["result"]



    if final:

        save_scraper_run(final)