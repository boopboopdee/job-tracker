import requests
from bs4 import BeautifulSoup


IGNORE_WORDS = [

    "about",
    "values",
    "culture",
    "mission",
    "press",
    "news",
    "blog",
    "investors"

]


JOB_WORDS = [

    "jobs",
    "careers",
    "openings",
    "positions",
    "opportunities",
    "apply"

]



def find_career_pages(url):

    pages = []


    try:

        response = requests.get(
            url,
            timeout=10
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        for link in soup.find_all("a"):


            href = link.get("href")


            text = link.text.lower()


            if not href:
                continue



            combined = (
                href.lower()
                +
                text
            )


            if any(
                word in combined
                for word in JOB_WORDS
            ):


                if not any(
                    bad in combined
                    for bad in IGNORE_WORDS
                ):

                    pages.append(href)



    except Exception as e:

        print(
            "Scanner error:",
            e
        )



    return list(
        set(pages)
    )