# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

import sqlite3

import os

from config import DATABASE_URL



# ---------------------------------
# CREATE DATABASE CONNECTION
# ---------------------------------

def get_connection():


    # ---------------------------------
    # LOCAL DEVELOPMENT
    # SQLITE DATABASE
    # ---------------------------------

    if DATABASE_URL.endswith(".db"):

        connection = sqlite3.connect(

            DATABASE_URL

        )

        connection.execute(
            "PRAGMA journal_mode=WAL;"
        )

        connection.execute(
            "PRAGMA synchronous=NORMAL;"
        )

        connection.row_factory = sqlite3.Row

        # ---------------------------------
        # SQLITE PERFORMANCE SETTINGS
        # ---------------------------------

        connection.execute(
            "PRAGMA journal_mode=WAL;"
        )

        connection.execute(
            "PRAGMA synchronous=NORMAL;"
        )

        connection.execute(
            "PRAGMA cache_size=-64000;"
        )



    # ---------------------------------
    # PRODUCTION
    # POSTGRESQL DATABASE
    # ---------------------------------

    else:


        import psycopg2

        from psycopg2.extras import RealDictCursor



        connection = psycopg2.connect(

            DATABASE_URL,

            cursor_factory=RealDictCursor

        )



    return connection