# ---------------------------------
# ATS DETECTOR
# Detects company recruiting platform
# ---------------------------------

import requests
from bs4 import BeautifulSoup



def detect_ats(url):

    result = {

        "platform": "custom",

        "parser_type": "custom",

        "board": None

    }


    if not url:

        return result



    try:

        response = requests.get(

            url,

            timeout=15,

            headers={
                "User-Agent":
                "Mozilla/5.0"
            }

        )


        html = response.text.lower()


        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )


        links = [

            a.get("href")

            for a in soup.find_all("a")

            if a.get("href")

        ]



        # ---------------------------------
        # GREENHOUSE
        # ---------------------------------

        for link in links:


            if "greenhouse.io" in link:


                parts = link.split("/")


                board = parts[-1]


                return {


                    "platform":
                    "greenhouse_api",


                    "parser_type":
                    "greenhouse_api",


                    "board":
                    board

                }




        # ---------------------------------
        # LEVER
        # ---------------------------------

        if "jobs.lever.co" in html:


            return {


                "platform":
                "lever",


                "parser_type":
                "lever"


            }




        # ---------------------------------
        # WORKDAY
        # ---------------------------------

        if "myworkdayjobs.com" in html:


            return {


                "platform":
                "workday",


                "parser_type":
                "workday"


            }




        # ---------------------------------
        # ASHBY
        # ---------------------------------

        if "ashbyhq.com" in html:


            return {


                "platform":
                "ashby",


                "parser_type":
                "ashby"


            }




        # ---------------------------------
        # SMART RECRUITERS
        # ---------------------------------

        if "smartrecruiters.com" in html:


            return {


                "platform":
                "smartrecruiters",


                "parser_type":
                "smartrecruiters"


            }




    except Exception as error:


        print(
            "ATS ERROR:",
            error
        )

    return {

        "platform": "custom",

        "parser_type": "custom",

        "board": None

    }