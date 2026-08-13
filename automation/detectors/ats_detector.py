import requests

from bs4 import BeautifulSoup



def detect_ats(url):


    result = {

        "platform":
        "custom",

        "parser_type":
        "custom",

        "board":
        ""

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



        # -----------------------------
        # GREENHOUSE
        # -----------------------------

        for link in links:


            if "greenhouse.io" in link:


                board = (

                    link

                    .split("/")

                    [-1]

                )


                return {


                    "platform":
                    "greenhouse",


                    "parser_type":
                    "greenhouse",


                    "board":
                    board

                }



        # -----------------------------
        # LEVER
        # -----------------------------

        if "jobs.lever.co" in html:


            return {


                "platform":
                "lever",


                "parser_type":
                "lever"

            }



        # -----------------------------
        # WORKDAY
        # -----------------------------

        if "myworkdayjobs.com" in html:


            return {


                "platform":
                "workday",


                "parser_type":
                "workday"

            }



        # -----------------------------
        # ASHBY
        # -----------------------------

        if "ashbyhq.com" in html:


            return {


                "platform":
                "ashby",


                "parser_type":
                "ashby"

            }



    except Exception as error:


        print(
            "ATS ERROR:",
            error
        )



    return result