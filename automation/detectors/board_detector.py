# ---------------------------------
# BOARD DETECTOR
# ---------------------------------

from urllib.parse import urlparse


def detect_board(url):

    parsed = urlparse(url)

    parts = parsed.path.strip("/").split("/")


    if "greenhouse" in parsed.netloc:

        if "boards" in parts:

            return parts[parts.index("boards")+1]


    elif "jobs.lever.co" in parsed.netloc:

        return parts[0]


    elif "ashbyhq.com" in parsed.netloc:

        return parts[0]


    return None