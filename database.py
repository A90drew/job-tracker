import psycopg
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_all_jobs():
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM jobs;")

    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return jobs

def add_job_to_db(role, company, deadline):
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO jobs (role, company, status, deadline)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """,
        (role, company, "Submitted", deadline)
        )
    created_job = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return created_job

def get_open_jobs():
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE deadline >= CURRENT_DATE
        ORDER BY deadline;
        """
    )
    current_open_jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return current_open_jobs

def not_applied_open():
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE status ='Not submitted'
         AND deadline >= CURRENT_DATE
        ORDER BY deadline;
        """
    )
    current_not_applied = cursor.fetchall()
    cursor.close()
    connection.close()
    return current_not_applied
