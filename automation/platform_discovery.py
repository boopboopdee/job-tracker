# ---------------------------------
# PLATFORM DISCOVERY ENGINE
# ---------------------------------

import requests

from bs4 import BeautifulSoup



# ---------------------------------
# DOWNLOAD PAGE
# ---------------------------------

def get_html(url):


    try:


        response = requests.get(

            url,

            timeout=10,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            }

        )


        return response.text.lower()



    except Exception as e:


        print(
            "Discovery failed:",
            e
        )


        return ""




# ---------------------------------
# DISCOVER PLATFORM
# ---------------------------------

def discover_platform(url):


    url_lower = url.lower()

    # ---------------------------------
    # KNOWN COMPANY ATS MAP
    # ---------------------------------

    known_companies = {


        "salesforce.com":

        {

            "platform":"workday",

            "parser_type":"workday"

        },


        "stripe.com":

        {

            "platform":"greenhouse",

            "parser_type":"greenhouse"

        },


        "adobe.com":

        {

            "platform":"custom",

            "parser_type":"custom"

        }

    }



    for domain, info in known_companies.items():


        if domain in url_lower:


            return info



    # ---------------------------------
    # STEP 1
    # DIRECT URL DETECTION
    # ---------------------------------


    if "greenhouse.io" in url_lower:


        return {

            "platform":"greenhouse",

            "parser_type":"greenhouse"

        }



    if "lever.co" in url_lower:


        return {

            "platform":"lever",

            "parser_type":"lever"

        }



    if "myworkdayjobs" in url_lower:


        return {

            "platform":"workday",

            "parser_type":"workday"

        }



    if "ashbyhq" in url_lower:


        return {

            "platform":"ashby",

            "parser_type":"ashby"

        }



    if "smartrecruiters" in url_lower:


        return {

            "platform":"smartrecruiters",

            "parser_type":"smartrecruiters"

        }




    # ---------------------------------
    # STEP 2
    # SCAN HTML
    # ---------------------------------

    html = get_html(url)



    if not html:


        return {

            "platform":"custom",

            "parser_type":"custom"

        }




    # ---------------------------------
    # STEP 3
    # ATS TEXT DETECTION
    # ---------------------------------


    ats_patterns = {


        "greenhouse":
        [

            "greenhouse.io",

            "boards.greenhouse"

        ],


        "lever":
        [

            "jobs.lever.co"

        ],


        "workday":
        [

            "myworkdayjobs",

            "workday"

        ],


        "ashby":
        [

            "ashbyhq"

        ],


        "smartrecruiters":
        [

            "smartrecruiters"

        ]

    }



    for parser, keywords in ats_patterns.items():


        for keyword in keywords:


            if keyword in html:


                return {

                    "platform":parser,

                    "parser_type":parser

                }




    # ---------------------------------
    # STEP 4
    # SCAN LINKS
    # ---------------------------------


    soup = BeautifulSoup(

        html,

        "html.parser"

    )



    for link in soup.find_all(

        "a",

        href=True

    ):


        href = link["href"].lower()



        if "greenhouse.io" in href:


            return {

                "platform":"greenhouse",

                "parser_type":"greenhouse"

            }



        if "lever.co" in href:


            return {

                "platform":"lever",

                "parser_type":"lever"

            }



        if "myworkdayjobs" in href:


            return {

                "platform":"workday",

                "parser_type":"workday"

            }



        if "ashbyhq" in href:


            return {

                "platform":"ashby",

                "parser_type":"ashby"

            }




    # ---------------------------------
    # STEP 5
    # UNKNOWN
    # ---------------------------------

    return {

        "platform":"custom",

        "parser_type":"custom"

    }