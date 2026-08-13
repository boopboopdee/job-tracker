# ---------------------------------
# PLATFORM DETECTOR
# ---------------------------------


def detect_platform(url):


    # -----------------------------
    # NO URL PROVIDED
    # -----------------------------

    if not url:

        return "custom"



    url = str(url).lower()



    # -----------------------------
    # PLATFORM CHECK
    # -----------------------------


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