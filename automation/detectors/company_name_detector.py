# ---------------------------------
# COMPANY NAME DETECTOR
# ---------------------------------

from urllib.parse import urlparse


def detect_company_name(url):

    parsed = urlparse(url)

    host = parsed.netloc

    host = host.replace("www.","")

    host = host.split(".")[0]

    return host.title()