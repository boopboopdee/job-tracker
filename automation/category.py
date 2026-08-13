# ---------------------------------
# JOB CATEGORY CLASSIFIER
# ---------------------------------


def get_category(title):


    title = title.lower()



    if "marketing" in title:

        return "Marketing Analytics"



    if "business intelligence" in title:

        return "Business Intelligence"



    if "data analyst" in title:

        return "Data Analytics"



    if "revenue operations" in title:

        return "Revenue Operations"



    if "growth" in title:

        return "Growth"



    if "crm" in title:

        return "CRM"



    if "customer insights" in title:

        return "Customer Insights"



    if "product marketing" in title:

        return "Product Marketing"



    if "sales operations" in title:

        return "Sales Operations"



    if "account executive" in title:

        return "Sales"



    if "account manager" in title:

        return "Sales"



    return "Other"