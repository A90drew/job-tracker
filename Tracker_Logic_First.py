import json
from datetime import date

jobs_tracker = [
    {
        "Id": 1,
        "Role": "Google Data Center Technician",
        "Company": "Google",
        "Status": "Not submitted", #evetually this will be changed
        "Posted": "2026-09-01",
        "Deadline": "2026-11-01"
    },
    {
        "Id": 2,
        "Role": "Amazon Cloude Architect",
        "Company": "Amazon",
        "Status": "Submitted",
        "Posted": "2026-09-01",
        "Deadline": "2026-12-01"
    },
    {
        "Id": 3,
        "Role": "Rakuten Solutions Architect",
        "Company": "Amazon",
        "Status": "Not submitted",
        "Posted": "2025-09-01",
        "Deadline": "2025-12-01"
    }
]
#JSON file saves
def save_jobs_to_file(jobs_tracker, filename):
    with open(filename, "w") as file:
        json.dump(jobs_tracker, file, indent=4)

def load_jobs_from_file(filename):
    with open(filename, "r") as file:
        jobs_tracker = json.load(file)
    return jobs_tracker



jobs_tracker = load_jobs_from_file("jobs.json")

def open_jobs(jobs):
    jobs_open = []
    current_time = str(date.today())
    for x in jobs:
        if x["Posted"] == None:
            continue
        if x["Deadline"] >= current_time and x["Posted"] <= current_time:
            x["Availability"] = "Open"
            jobs_open.append(x)

    if not jobs_open:
        return "No open jobs currently"

    return jobs_open


def open_not_applied(current_open):
    not_applied = []
    if isinstance(current_open, list):
        for x in current_open:
            if x["Status"] == "Not submitted":
                not_applied.append(x)

        if not not_applied:
            return "Applied to all open jobs"
        return not_applied
    
    else:
        return "No open jobs currently"

# below was for testing
# big = open_not_applied(open_jobs(jobs_tracker))
# print(big)
# end of code testing

def add_jobs(jobs_tracker, role, company, deadline): # this function takes info to add a new job
    jobs_id = []
    for x in jobs_tracker:
        IDs = x['Id'] #want to grab ID
        jobs_id.append(IDs)
    added_job = {
        "Id": max(jobs_id) +1,
        "Role": role,
        "Company": company,
        "Status": "Submitted", #assumes job were adding was applied to
        "Posted": None,
        "Deadline": deadline
    }

    jobs_tracker.append(added_job)
    save_jobs_to_file(jobs_tracker, "jobs.json")
    return added_job

# Basicaly job_tracker only needed for the max ID to correctly assign new ID
# Thereforeparameter job_tracker WILL take jobs_tracker as its parameter
# role, company, deadline is what we add
# Assumes that we applied to job therefore Posted is irrelevant


# below was for testing
# print(add_jobs(jobs_tracker, "Cloud Architect", "Hennge", "2026-12-09"))
# print("Seperated")
# print(jobs_tracker)
# end of code testing