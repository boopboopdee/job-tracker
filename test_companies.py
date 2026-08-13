from automation.company_loader import get_active_companies


companies = get_active_companies()


for company in companies:

    print(company)