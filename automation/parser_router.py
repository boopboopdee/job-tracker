# ---------------------------------
# PARSER ROUTER
# Automatically selects correct parser
# ---------------------------------

from automation.parser_registry import PARSERS

from automation.intelligence.ats_detector import detect_ats



# ---------------------------------
# NORMALIZE PARSER NAMES
# ---------------------------------

def normalize_parser(parser):

    if not parser:
        return None


    parser = parser.lower()


    if parser == "greenhouse_api":

        return "greenhouse"


    return parser



# ---------------------------------
# GET JOBS FOR COMPANY
# ---------------------------------

def get_jobs(company):


    # ---------------------------------
    # GET COMPANY DATABASE VALUES
    # ---------------------------------

    platform = company.get(
        "platform"
    )


    parser_type = company.get(
        "parser_type"
    )


    # ---------------------------------
    # NORMALIZE VALUES
    # ---------------------------------

    platform = normalize_parser(
        platform
    )


    parser_type = normalize_parser(
        parser_type
    )



    # ---------------------------------
    # USE DATABASE VALUE FIRST
    # ---------------------------------

    if not parser_type:

        parser_type = platform



    # ---------------------------------
    # DETECT ATS IF UNKNOWN
    # ---------------------------------

    if not parser_type:


        url = company.get(
            "url"
        )


        if url:


            print(
                "Detecting ATS:",
                company["name"]
            )


            detected = detect_ats(
                url
            )


            company.update(
                detected
            )


            parser_type = detected.get(
                "parser_type"
            )



    # ---------------------------------
    # NORMALIZE AGAIN AFTER DETECTION
    # ---------------------------------

    parser_type = normalize_parser(
        parser_type
    )



    # ---------------------------------
    # FIND PARSER
    # ---------------------------------

    parser = PARSERS.get(
        parser_type
    )



    if not parser:


        print(
            "PARSER NOT FOUND:",
            company["name"],
            parser_type
        )


        return []



    print(
        "Using parser:",
        parser_type,
        "for",
        company["name"]
    )



    # ---------------------------------
    # RUN PARSER
    # ---------------------------------

    return parser(
        company
    )