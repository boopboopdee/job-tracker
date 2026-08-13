# ---------------------------------
# URL ANALYZER
# ---------------------------------

from urllib.parse import urlparse


def analyze_url(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.strip("/")


    company = ""

    platform = "custom"

    board = ""

    parser = "custom"


    # ---------------------------------
    # GREENHOUSE
    # ---------------------------------

    if "greenhouse.io" in domain:

        platform = "greenhouse_api"

        parser = "greenhouse_api"

        pieces = path.split("/")

        if "boards" in pieces:

            board = pieces[pieces.index("boards")+1]

        elif "job-boards.greenhouse.io" in domain:

            board = pieces[0]

        company = board.title()


    # ---------------------------------
    # LEVER
    # ---------------------------------

    elif "jobs.lever.co" in domain:

        platform = "lever"

        parser = "lever"

        board = path.split("/")[0]

        company = board.title()


    # ---------------------------------
    # WORKDAY
    # ---------------------------------

    elif "myworkdayjobs.com" in domain:

        platform = "workday"

        parser = "workday"

        company = domain.split(".")[0].title()


    # ---------------------------------
    # ASHBY
    # ---------------------------------

    elif "ashbyhq.com" in domain:

        platform = "ashby"

        parser = "ashby"

        board = path.split("/")[0]

        company = board.title()


    # ---------------------------------
    # SMARTRECRUITERS
    # ---------------------------------

    elif "smartrecruiters.com" in domain:

        platform = "smartrecruiters"

        parser = "smartrecruiters"

        board = path.split("/")[-1]

        company = board.title()


    else:

        company = domain.replace("www.","")


    return {

        "company": company,

        "platform": platform,

        "parser": parser,

        "board": board

    }