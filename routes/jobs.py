from flask import Blueprint, render_template, request, redirect
from urllib.parse import urlencode

from database import get_connection


jobs_bp = Blueprint(
    "jobs",
    __name__
)

# ---------------------------------
# GET MULTI-SELECT VALUES
# ---------------------------------

def get_selected(name):

    values = request.args.getlist(name)

    values = [v for v in values if v]

    return values


# ---------------------------------
# BUILD SQL PLACEHOLDERS
# ---------------------------------

def sql_placeholders(values):
    return ",".join(["%s"] * len(values))


# ---------------------------------
# GET DISTINCT VALUES
# FOR CHECKBOX FILTERS
# ---------------------------------

def get_filter_lists(cursor):

    filters = {}

    columns = {

        "companies": "company",

        "statuses": "status",

        "locations": "location",

        "remote_types": "remote",

        "sources": "job_source"

    }

    for key, column in columns.items():

        cursor.execute(f"""
        SELECT DISTINCT {column}

        FROM jobs

        WHERE {column} IS NOT NULL

        AND {column} != ''

        ORDER BY {column}
        """)

        filters[key] = [
            row[column]
            for row in cursor.fetchall()
        ]

    return filters

# ---------------------------------
# VIEW ALL JOBS + SEARCH + FILTERS
# ---------------------------------

@jobs_bp.route("/jobs")
def jobs():


    connection = get_connection()

    cursor = connection.cursor()

    # ---------------------------------
    # GLOBAL SEARCH
    # ---------------------------------

    search = request.args.get(
        "search",
        ""
    )

    # ---------------------------------
    # MULTI-SELECT FILTERS
    # ---------------------------------

    selected_companies = get_selected(
        "company"
    )

    selected_statuses = get_selected(
        "status"
    )

    selected_locations = get_selected(
        "location"
    )

    selected_remote = get_selected(
        "remote"
    )

    selected_sources = get_selected(
        "source"
    )

    # Column-specific filters
    c_company = request.args.get("c_company", "")
    c_title = request.args.get("c_title", "")
    c_location = request.args.get("c_location", "")
    c_salary = request.args.get("c_salary", "")
    c_source = request.args.get("c_source", "")
    c_favorite = request.args.get("c_favorite", "")

    # ---------------------------------
    # PAGINATION + SORTING
    # ---------------------------------

    page = request.args.get(
        "page",
        1,
        type=int
    )

    per_page = 25

    offset = (page - 1) * per_page

    # ---------------------------------
    # PRIMARY SORT
    # ---------------------------------

    primary_sort = request.args.get(
        "primary_sort",
        "date_found"
    )

    primary_direction = request.args.get(
        "primary_direction",
        "DESC"
    )

    # ---------------------------------
    # SECONDARY SORT
    # ---------------------------------

    secondary_sort = request.args.get(
        "secondary_sort",
        ""
    )

    secondary_direction = request.args.get(
        "secondary_direction",
        "ASC"
    )

    # ---------------------------------
    # BASE FILTER (WHERE clause)
    # ---------------------------------

    filter_query = """
    WHERE 1=1
    """

    parameters = []

    allowed_sort_columns = {

        "id": "id",

        "company": "company",

        "title": "title",

        "location": "location",

        "remote": "remote",

        "salary": "salary",

        "status": "status",

        "favorite": "favorite",

        "source": "job_source",

        "date_found": "date_found"

    }

    # ---------------------------------
    # BUILD MULTI-LEVEL SORT
    # PRIMARY
    # SECONDARY
    # FINAL NEWEST ID TIE BREAKER
    # ---------------------------------

    sort_parts = []

    if primary_sort in allowed_sort_columns:
        sort_parts.append(
            f"{allowed_sort_columns[primary_sort]} {primary_direction}"
        )

    if (
            secondary_sort
            and secondary_sort in allowed_sort_columns
            and secondary_sort != primary_sort
    ):
        sort_parts.append(
            f"{allowed_sort_columns[secondary_sort]} {secondary_direction}"
        )

    # ALWAYS KEEP NEWEST ADDED FIRST WHEN VALUES MATCH

    sort_parts.append(
        "id DESC"
    )

    order_by = ", ".join(sort_parts)



    # ---------------------------------
    # SEARCH FILTER
    # Searches every word separately
    # ---------------------------------

    if search:

        keywords = search.split()

        filter_query += "\nAND (\n"

        search_conditions = []

        for word in keywords:
            search_conditions.append("""
            (
                company LIKE %s
                OR title LIKE %s
                OR location LIKE %s
                OR salary LIKE %s
                OR job_source LIKE %s
            )
            """)

            parameters.extend([
                f"%{word}%",  # company
                f"%{word}%",  # title
                f"%{word}%",  # location
                f"%{word}%",  # salary
                f"%{word}%"  # job_source
            ])

        # Match ANY of the words
        filter_query += " OR ".join(search_conditions)

        filter_query += "\n)\n"

    # ---------------------------------
    # COLUMN SPECIFIC FILTERS
    # ---------------------------------

    if c_company:
        filter_query += " AND company LIKE %s"
        parameters.append(f"%{c_company}%")

    if c_title:
        filter_query += " AND title LIKE %s"
        parameters.append(f"%{c_title}%")

    if c_location:
        filter_query += " AND location LIKE %s"
        parameters.append(f"%{c_location}%")

    if c_salary:
        filter_query += " AND salary LIKE %s"
        parameters.append(f"%{c_salary}%")

    if c_source:
        filter_query += " AND job_source LIKE %s"
        parameters.append(f"%{c_source}%")

    if c_favorite:
        if c_favorite == "Saved":
            filter_query += " AND favorite = 1"
        elif c_favorite == "Not Saved":
            filter_query += " AND favorite = 0"

    # ---------------------------------
    # COMPANY CHECKBOX FILTER
    # ---------------------------------

    if selected_companies:
        placeholders = sql_placeholders(selected_companies)

        filter_query += f"""
        AND company IN ({placeholders})
        """

        parameters.extend(selected_companies)

    # ---------------------------------
    # STATUS CHECKBOX FILTER
    # ---------------------------------

    if selected_statuses:
        placeholders = sql_placeholders(selected_statuses)

        filter_query += f"""
        AND status IN ({placeholders})
        """

        parameters.extend(selected_statuses)

    # ---------------------------------
    # LOCATION CHECKBOX FILTER
    # ---------------------------------

    if selected_locations:
        placeholders = sql_placeholders(selected_locations)

        filter_query += f"""
        AND location IN ({placeholders})
        """

        parameters.extend(selected_locations)

    # ---------------------------------
    # REMOTE CHECKBOX FILTER
    # ---------------------------------

    if selected_remote:
        placeholders = sql_placeholders(selected_remote)

        filter_query += f"""
        AND remote IN ({placeholders})
        """

        parameters.extend(selected_remote)

    # ---------------------------------
    # SOURCE CHECKBOX FILTER
    # ---------------------------------

    if selected_sources:
        placeholders = sql_placeholders(selected_sources)

        filter_query += f"""
        AND job_source IN ({placeholders})
        """

        parameters.extend(selected_sources)



    # ---------------------------------
    # COUNT TOTAL
    # ---------------------------------
    cursor.execute(
        "SELECT COUNT(*) AS total FROM jobs " + filter_query,
        parameters
    )

    total_jobs = cursor.fetchone()["total"]
    total_pages = (total_jobs + per_page - 1) // per_page if total_jobs > 0 else 1

    # ---------------------------------
    # GET PAGINATED DATA
    # ---------------------------------
    # ---------------------------------
    # BUILD SORTED QUERY
    # ---------------------------------

    data_query = f"""
    SELECT
        id,
        company,
        title,
        location,
        remote,
        salary,
        status,
        url,
        favorite,
        job_source,
        date_found

    FROM jobs

    {filter_query}

    ORDER BY {order_by}

    LIMIT %s

    OFFSET %s

    """

    data_parameters = parameters + [per_page, offset]

    print("\nQUERY:")
    print(data_query)

    print("\nPARAMETERS:")
    print(data_parameters)

    cursor.execute(data_query, data_parameters)

    jobs = cursor.fetchall()

    # ---------------------------------
    # LOAD FILTER LISTS
    # BEFORE CLOSING DATABASE
    # ---------------------------------

    filters = get_filter_lists(cursor)

    # ---------------------------------
    # KEEP FILTERS WHEN SORTING
    # ---------------------------------

    query_parameters = request.args.to_dict()

    query_parameters.pop(
        "primary_sort",
        None
    )

    query_parameters.pop(
        "primary_direction",
        None
    )

    from urllib.parse import urlencode

    args = request.args.to_dict(flat=False)

    # Remove page before rebuilding the query string
    args.pop("page", None)

    query_string = urlencode(args, doseq=True)

    connection.close()

    return render_template(
        "jobs.html",
        jobs=jobs,
        page=page,
        total_pages=total_pages,
        total_jobs=total_jobs,
        search=search,
        c_company=c_company,
        c_title=c_title,
        c_location=c_location,
        c_salary=c_salary,
        c_source=c_source,
        c_favorite=c_favorite,
        selected_companies=selected_companies,
        selected_statuses=selected_statuses,
        selected_locations=selected_locations,
        selected_remote=selected_remote,
        selected_sources=selected_sources,

        primary_sort=primary_sort,
        primary_direction=primary_direction,

        secondary_sort=secondary_sort,
        secondary_direction=secondary_direction,

        filters=filters,
        query_string=query_string,
    )


@jobs_bp.route(
    "/add-job",
    methods=["GET","POST"]
)
def add_job():


    if request.method == "POST":


        company = request.form["company"]

        title = request.form["title"]

        location = request.form["location"]

        remote = request.form["remote"]

        salary = request.form["salary"]

        url = request.form["url"]


        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO jobs
    
            (
            company,
            title,
            location,
            remote,
            salary,
            url,
            status
            )
    
            VALUES (%s,%s,%s,%s,%s,%s,%s)
    
            """,

            (
                company,
                title,
                location,
                remote,
                salary,
                url,
                "New"
            )
        )

        connection.commit()

        connection.close()


        return redirect("/jobs")


    return render_template(
        "add_job.html"
    )

@jobs_bp.route("/delete/<int:id>")
def delete_job(id):


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        "DELETE FROM jobs WHERE id=%s",

        (id,)

    )


    connection.commit()

    connection.close()


    return redirect(request.referrer or "/jobs")



@jobs_bp.route(
    "/edit/<int:id>",
    methods=["GET","POST"]
)
def edit_job(id):

    connection = get_connection()

    cursor = connection.cursor()


    if request.method == "POST":

        status = request.form["status"]

        notes = request.form["notes"]


        cursor.execute(
        """
        UPDATE jobs

        SET status=%s,
            notes=%s

        WHERE id=%s

        """,
        (
            status,
            notes,
            id
        ))

        connection.commit()

        connection.close()

        return redirect("/jobs")


    cursor.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (id,)
    )


    job = cursor.fetchone()


    connection.close()


    return render_template(
        "edit_job.html",
        job=job
    )

# ---------------------------------
# SAVED / FAVORITE JOBS
# ---------------------------------

@jobs_bp.route("/saved-jobs")
def saved_jobs():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM jobs

        WHERE favorite = 1

        ORDER BY date_found DESC

        """
    )


    jobs = cursor.fetchall()


    connection.close()


    return render_template(
        "saved_jobs.html",
        jobs=jobs
    )

# ---------------------------------
# APPLIED JOBS
# ---------------------------------

@jobs_bp.route("/applied-jobs")
def applied_jobs():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM jobs

        WHERE status = 'Applied'

        ORDER BY date_found DESC

        """
    )


    jobs = cursor.fetchall()


    connection.close()


    return render_template(
        "applied_jobs.html",
        jobs=jobs
    )

# ---------------------------------
# FAVORITES PAGE
# ---------------------------------

@jobs_bp.route("/favorites")
def favorites():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM jobs

        WHERE favorite = 1

        ORDER BY date_found DESC

        """
    )


    jobs = cursor.fetchall()

    connection.close()


    return render_template(
        "saved_jobs.html",
        jobs=jobs
    )

# ---------------------------------
# APPLICATIONS PAGE
# ---------------------------------

@jobs_bp.route("/applications")
def applications():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM jobs

        WHERE status = 'Applied'

        ORDER BY date_found DESC

        """
    )


    jobs = cursor.fetchall()

    connection.close()


    return render_template(
        "applied_jobs.html",
        jobs=jobs
    )


# ---------------------------------
# TOGGLE FAVORITE
# ---------------------------------

@jobs_bp.route("/favorite/<int:id>")
def favorite_job(id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE jobs

        SET favorite =

        CASE

        WHEN favorite = 1 THEN 0

        ELSE 1

        END


        WHERE id=%s

        """,

        (id,)

    )

    connection.commit()

    connection.close()

    return redirect(request.referrer or "/jobs")



# ---------------------------------
# UPDATE JOB STATUS
# ---------------------------------

@jobs_bp.route("/update-status/<int:id>/<status>")
def update_status(id, status):


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """

        UPDATE jobs

        SET status=%s

        WHERE id=%s

        """,

        (
            status,
            id
        )

    )


    connection.commit()

    connection.close()


    return redirect(request.referrer or "/jobs")
