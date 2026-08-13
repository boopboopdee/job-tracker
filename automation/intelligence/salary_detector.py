import re


def extract_salary(text):

    matches = re.findall(

        r"\$[\d,]+",

        text

    )


    if matches:

        return matches[0]


    return "Unknown"