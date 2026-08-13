from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from automation.ats_profiles import (
    GREENHOUSE_PROFILES,
    WORKDAY_PROFILES
)



# ---------------------------------
# DETECT COMPANY ATS
# ---------------------------------

def detect_company(url):


    result = {

        "platform": "custom",

        "parser_type": "custom",

        "board": ""

    }


    url_lower = url.lower()

    # ---------------------------------
    # KNOWN GREENHOUSE COMPANIES
    # ---------------------------------

    for domain, board in GREENHOUSE_PROFILES.items():

        if domain in url_lower:
            return {

                "platform": "greenhouse",

                "parser_type": "greenhouse",

                "board": board

            }

    # ---------------------------------
    # KNOWN WORKDAY COMPANIES
    # ---------------------------------

    for domain, board in WORKDAY_PROFILES.items():

        if domain in url_lower:
            return {

                "platform": "workday",

                "parser_type": "workday",

                "board": board

            }

    # ---------------------------------
    # DIRECT ATS URLS
    # ---------------------------------

    if "greenhouse.io" in url_lower:


        result["platform"] = "greenhouse"

        result["parser_type"] = "greenhouse"

        result["board"] = extract_board(url)


        return result



    if "lever.co" in url_lower:


        result["platform"] = "lever"

        result["parser_type"] = "lever"


        return result

    if "myworkdayjobs.com" in url_lower:
        result["platform"] = "workday"

        result["parser_type"] = "workday"

        result["board"] = extract_board(url)

        return result



    # ---------------------------------
    # SCAN CAREER PAGE
    # ---------------------------------

    detected = scan_for_ats(url)


    if detected:

        return detected



    return result




# ---------------------------------
# SCAN WEBSITE FOR ATS
# ---------------------------------

def scan_for_ats(url):


    try:

        response = requests.get(

            url,

            timeout=15,

            headers={
                "User-Agent":
                    "Mozilla/5.0"
            },

            allow_redirects=True

        )

        # ---------------------------------
        # CHECK FINAL REDIRECT URL
        # ---------------------------------

        final_url = response.url.lower()

        if "greenhouse.io" in final_url:
            return {

                "platform":
                    "greenhouse",

                "parser_type":
                    "greenhouse",

                "board":
                    extract_board(final_url)

            }

        if "lever.co" in final_url:
            return {

                "platform":
                    "lever",

                "parser_type":
                    "lever",

                "board":
                    ""

            }

        if "myworkdayjobs.com" in final_url:
            return {

                "platform":
                    "workday",

                "parser_type":
                    "workday",

                "board":
                    extract_board(final_url)

            }


        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )



        links = []


        for a in soup.find_all(
            "a",
            href=True
        ):


            links.append(
                a["href"]
            )



        # -------------------------
        # GREENHOUSE
        # -------------------------

        for link in links:


            if "greenhouse.io" in link.lower():


                return {

                    "platform":
                        "greenhouse",

                    "parser_type":
                        "greenhouse",

                    "board":
                        extract_board(link)

                }




        # -------------------------
        # LEVER
        # -------------------------

        for link in links:


            if "lever.co" in link.lower():


                return {

                    "platform":
                        "lever",

                    "parser_type":
                        "lever",

                    "board":
                        ""

                }

        # -------------------------
        # WORKDAY
        # -------------------------

        page = response.text.lower()

        url_lower = url.lower()

        # -------------------------
        # WORKDAY PROFILES
        # -------------------------

        for domain, board in WORKDAY_PROFILES.items():

            if domain in url_lower and "myworkdayjobs.com" in url_lower:
                return {

                    "platform":
                        "workday",

                    "parser_type":
                        "workday",

                    "board":
                        board

                }

        # -------------------------
        # WORKDAY HTML DETECTION
        # -------------------------

        if "myworkdayjobs" in page:
            return {

                "platform":
                    "workday",

                "parser_type":
                    "workday",

                "board":
                    extract_board(response.url)

            }


    except Exception as e:


        print(
            "ATS scan failed:",
            e
        )


    return None




# ---------------------------------
# EXTRACT BOARD
# ---------------------------------

def extract_board(url):


    parsed = urlparse(url)


    host = parsed.netloc.lower()


    path = parsed.path.strip("/").split("/")



    # ---------------------------------
    # GREENHOUSE
    # ---------------------------------

    if "greenhouse.io" in host:


        for part in path:


            if part not in [

                "boards",

                "jobs",

                "job-boards"

            ]:

                return part




    # ---------------------------------
    # LEVER
    # ---------------------------------

    if "lever.co" in host:


        return path[0]




    # ---------------------------------
    # WORKDAY
    # ---------------------------------

    if "myworkdayjobs" in host:


        return host.split(".")[0]




    return ""

# ---------------------------------
# EXTRACT COMPANY NAME
# ---------------------------------

def extract_company_name(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    domain = domain.replace(
        "www.",
        ""
    )

    company = domain.split(".")[0]

    return company.title()