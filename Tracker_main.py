from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import (
    get_all_jobs, 
    add_job_to_db, 
    get_open_jobs, 
    not_applied_open, 
    update_job_status,
    delete_job)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewJob(BaseModel): #creating input settings for inputting job
    role: str
    company: str
    deadline: date
    url: str

class StatusUpdate(BaseModel):
    status: str


@app.post("/jobs") #creating a record so it goes into Jobs even though it's auto submitted
def create_job(new_job: NewJob): #new_job MUST follow NewJob's rules
    created_job = add_job_to_db(
        new_job.role,
        new_job.company,
        new_job.deadline,
        new_job.url
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

@app.patch("/jobs/{job_id}/status")
def change_job_statuse(job_id: int, status_update: StatusUpdate):
    updated_job = update_job_status(
        job_id,
        status_update.status
    )
    return updated_job

@app.delete("/jobs/{job_id}")
def will_delete_job(job_id: int):
    deleting_job = delete_job(job_id)
    return deleting_job

# uvicorn Tracker_main:app --reload
# http://127.0.0.1:8000
# http://127.0.0.1:8000/docs