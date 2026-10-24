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

    named_jobs = []

    for job in jobs:
        named_jobs.append({
            "id": job[0],
            "role": job[1],
            "company": job[2],
            "status": job[3],
            "posted": job[4],
            "deadline": job[5]
        })
    cursor.close()
    connection.close()
    return named_jobs

def add_job_to_db(role, company, deadline, url):
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO jobs (role, company, status, deadline, url)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """,
        (role, company, "Submitted", deadline, url)
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

def update_job_status(job_id, status):
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE jobs
        SET status = %s
        WHERE id = %s
        RETURNING *;
        """,
        (status, job_id)
    )
    updated_job = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return updated_job

def delete_job(job_id):
    connection = psycopg.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM jobs
        WHERE id = %s
        RETURNING *;
        """,
        (job_id,)
    )
    deleted_job = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return deleted_job

