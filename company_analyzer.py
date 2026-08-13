# ---------------------------------
# COMPANY URL ANALYZER
# ---------------------------------

from urllib.parse import urlparse



# ---------------------------------
# EXTRACT COMPANY NAME
# ---------------------------------

def extract_company_name(url):


    domain = urlparse(url).netloc


    domain = domain.replace(
        "www.",
        ""
    )


    name = domain.split(".")[0]


    return name.title()



# ---------------------------------
# DETECT PLATFORM
# ---------------------------------

def detect_platform(url):


    url = url.lower()



    if "greenhouse" in url:

        return "greenhouse"



    elif "lever" in url:

        return "lever"



    elif "workday" in url:

        return "workday"



    elif "ashby" in url:

        return "ashby"



    else:

        return "custom"




# ---------------------------------
# EXTRACT BOARD NAME
# ---------------------------------

def extract_board(url):


    parts = url.split("/")



    for word in parts:


        if "greenhouse" in url.lower():

            return parts[-1]



        if "lever" in url.lower():

            return parts[-1]



    return None




# ---------------------------------
# ANALYZE COMPANY
# ---------------------------------

def analyze_company(url):


    return {


        "name": extract_company_name(url),


        "platform": detect_platform(url),


        "board": extract_board(url),


        "url": url,


        "active": 1


    }