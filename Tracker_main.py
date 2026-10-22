from fastapi import FastAPI
from database import get_all_jobs, add_job_to_db, get_open_jobs, not_applied_open
from pydantic import BaseModel
from datetime import date
#from Tracker_Logic_First import (
    #save_jobs_to_file,
    #load_jobs_from_file,
    #open_jobs,
    #open_not_applied,
    #add_jobs
#)

#import psycopg
#connection_string = "db=" #will be using PostgreSQL for my db

app = FastAPI()
#jobs_tracker = load_jobs_from_file("jobs.json") #temp db for fastAPI while we work on endpoints

class NewJob(BaseModel): #creating input settings for inputting job
    role: str
    company: str
    deadline: date


@app.post("/jobs") #creating a record so it goes into Jobs even though it's auto submitted
def create_job(new_job: NewJob): #new_job MUST follow NewJob's rules
    created_job = add_job_to_db(
        new_job.role,
        new_job.company,
        new_job.deadline
        )
    return created_job
    
    
@app.get("/")
def home():
    return "Jobs tracker API is working"

@app.get("/jobs")
def read_jobs():
    return get_all_jobs()

@app.get("/jobs/open")
def read_open_jobs():
    return get_open_jobs()

@app.get("/jobs/open/not-applied")
def read_open_not_applied():
    return not_applied_open()

# uvicorn Tracker_main:app --reload
# http://127.0.0.1:8000
# http://127.0.0.1:8000/docs