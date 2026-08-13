# ---------------------------------
# COMPANY MANAGEMENT ROUTES
# ---------------------------------

from flask import Blueprint, render_template, request, redirect

from database import get_connection

from automation.scraper import (
    process_company
)

from automation.companies import COMPANIES

companies_bp = Blueprint(
    "companies",
    __name__
)

# ---------------------------------
# SYNC SCRAPER COMPANIES
# ---------------------------------

@companies_bp.route("/sync-companies")
def sync_companies():

    connection = get_connection()
    cursor = connection.cursor()

    for company in COMPANIES:

        cursor.execute(
            """
            SELECT id
            FROM companies
            WHERE name=?
            """,
            (company["name"],)
        )

        exists = cursor.fetchone()

        # ---------------------------------
        # UPDATE EXISTING COMPANY
        # ---------------------------------

        if exists:

            cursor.execute(
                """
                UPDATE companies

                SET
                    platform=?,
                    board=?,
                    url=?,
                    parser_type=?,
                    active=1

                WHERE name=?
                """,
                (
                    company.get("platform"),
                    company.get("board"),
                    company.get("url"),
                    company.get("parser_type"),
                    company["name"]
                )
            )

        # ---------------------------------
        # ADD NEW COMPANY
        # ---------------------------------

        else:

            cursor.execute(
                """
                INSERT INTO companies
                (
                    name,
                    platform,
                    board,
                    url,
                    active,
                    parser_type
                )

                VALUES (?,?,?,?,?,?)
                """,
                (
                    company["name"],
                    company.get("platform"),
                    company.get("board"),
                    company.get("url"),
                    1,
                    company.get("parser_type")
                )
            )

    connection.commit()
    connection.close()

    return redirect("/companies")


# ---------------------------------
# SCAN SINGLE COMPANY
# ---------------------------------

@companies_bp.route(
    "/scan-company/<int:id>"
)
def scan_company(id):


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        (id,)
    )


    company_row = cursor.fetchone()


    connection.close()


    if not company_row:

        return redirect("/companies")



    company = {

        "name": company_row["name"],

        "platform": company_row["platform"],

        "parser_type": company_row["parser_type"],

        "board": company_row["board"],

        "url": company_row["url"]

    }



    # ---------------------------------
    # RUN FULL AI + ATS SCANNER
    # ---------------------------------

    result = process_company(company)



    return render_template(

        "company_scan_results.html",

        company=company,

        jobs=result["new_jobs"],

        saved_jobs=result["new_jobs"],

        found=result["found"],

        matching=result["matching"],

        added=result["saved"]

    )




# ---------------------------------
# VIEW COMPANIES
# ---------------------------------

@companies_bp.route("/companies")

def companies():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """

        SELECT *

        FROM companies

        ORDER BY name

        """
    )


    companies = cursor.fetchall()


    connection.close()


    return render_template(
        "companies.html",
        companies=companies
    )





# ---------------------------------
# ADD COMPANY FROM URL
# ---------------------------------

@companies_bp.route(
    "/add-company",
    methods=["POST"]
)
def add_company():

    url = request.form["url"]

    # ---------------------------------
    # AUTO DETECT INFORMATION
    # ---------------------------------

    from automation.company_detector import (
        detect_company,
        extract_company_name,
        extract_board
    )

    # ---------------------------------
    # AUTO DISCOVER PLATFORM
    # ---------------------------------

    from automation.platform_discovery import (
        discover_platform
    )

    info = discover_platform(url)

    from automation.intelligence.ats_detector import detect_ats

    # ---------------------------------
    # AUTO DETECT ATS
    # ---------------------------------

    ats = detect_ats(url)

    info.update(
        ats
    )

    # ---------------------------------
    # NORMALIZE ATS VALUES
    # ---------------------------------

    if info["platform"] == "greenhouse_api":
        info["platform"] = "greenhouse"

    if info["parser_type"] == "greenhouse_api":
        info["parser_type"] = "greenhouse"

    name = extract_company_name(url)

    board = extract_board(url)

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO companies
        (
            name,
            platform,
            board,
            url,
            active,
            parser_type
        )

        VALUES (?,?,?,?,?,?)
        """,
        (
            name,
            info["platform"],
            board,
            url,
            1,
            info["parser_type"]
        )
    )

    connection.commit()

    connection.close()

    return redirect("/companies")

# ---------------------------------
# SHOW EDIT COMPANY PAGE
# ---------------------------------

@companies_bp.route(
    "/edit-company/<int:id>",
    methods=["GET"]
)
def edit_company_page(id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM companies

        WHERE id=?

        """,
        (id,)
    )


    company = cursor.fetchone()


    connection.close()


    return render_template(
        "edit_company.html",
        company=company
    )

# ---------------------------------
# EDIT COMPANY
# ---------------------------------

@companies_bp.route(
    "/edit-company/<int:id>",
    methods=["POST"]
)
def edit_company(id):
    print("EDITING COMPANY ID:", id)

    print(
        "FORM DATA:",
        request.form
    )

    name = request.form["name"]

    platform = request.form["platform"]

    parser_type = request.form["parser_type"]

    board = request.form["board"]

    url = request.form["url"]


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE companies

        SET
            name=?,
            platform=?,
            parser_type=?,
            board=?,
            url=?

        WHERE id=?

        """,
        (
            name,
            platform,
            parser_type,
            board,
            url,
            id
        )
    )


    connection.commit()

    connection.close()


    return redirect("/companies")

# ---------------------------------
# DELETE COMPANY
# ---------------------------------

@companies_bp.route(
    "/delete-company/<int:id>",
    methods=["POST"]
)
def delete_company(id):


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM companies

        WHERE id=?

        """,
        (id,)
    )


    connection.commit()

    connection.close()


    return redirect("/companies")