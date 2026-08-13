# ---------------------------------
# PARSER REGISTRY
# ---------------------------------


from automation.parsers.greenhouse_api import (
    get_greenhouse_api_jobs
)


from automation.parsers.lever import (
    get_lever_jobs
)


from automation.parsers.workday import (
    get_workday_jobs
)


from automation.parsers.custom import (
    get_custom_jobs
)


from automation.parsers.ashby import (
    get_ashby_jobs
)


from automation.parsers.smartrecruiters import (
    get_smartrecruiters_jobs
)




PARSERS = {


    # GREENHOUSE

    "greenhouse_api":
    get_greenhouse_api_jobs,


    # keep compatibility

    "greenhouse":
    get_greenhouse_api_jobs,



    # LEVER

    "lever":
    get_lever_jobs,



    # WORKDAY

    "workday":
    get_workday_jobs,



    # ASHBY

    "ashby":
    get_ashby_jobs,



    # SMART RECRUITERS

    "smartrecruiters":
    get_smartrecruiters_jobs,



    # CUSTOM

    "custom":
    get_custom_jobs

}