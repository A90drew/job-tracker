# Job Application Tracker

A backend API for tracking job applications. The project began with Python and JSON storage and was later connected to PostgreSQL for persistent data storage.

## Technologies

- Python
- FastAPI
- PostgreSQL
- Psycopg
- Pydantic

## Features

- View all job applications
- Add new job applications
- View jobs with current or future deadlines
- View jobs that have not been submitted
- Preserve data after restarting the API

## Project Structure

- `Tracker_main.py` — FastAPI application and API endpoints
- `database.py` — PostgreSQL connection and database queries
- `database_test.py` — Tests the Python-to-PostgreSQL connection
- `Tracker_Logic_First.py` — Original JSON-based logic
- `jobs.json` — Original sample data

## Installation

Install the required packages:

```bash
python3 -m pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project folder:

```text
DATABASE_URL=dbname=job_tracker user=your_username
```

Replace `your_username` with your PostgreSQL username.

Do not commit the `.env` file to GitHub.

## Database Setup

Create a PostgreSQL database named:

```text
job_tracker
```

Create the `jobs` table:

```sql
CREATE TABLE jobs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role TEXT NOT NULL,
    company TEXT NOT NULL,
    status TEXT NOT NULL,
    posted DATE,
    deadline DATE
);
```

## Running the API

Start the FastAPI server:

```bash
uvicorn Tracker_main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Confirms that the API is running |
| GET | `/jobs` | Returns all jobs |
| POST | `/jobs` | Adds a new submitted job |
| GET | `/jobs/open` | Returns jobs with current or future deadlines |
| GET | `/jobs/open/not-applied` | Returns jobs not yet submitted with current or future deadlines |

## Example POST Request

```json
{
  "role": "Business Systems Analyst",
  "company": "Microsoft",
  "deadline": "2026-12-15"
}
```

New jobs are automatically assigned the status:

```text
Submitted
```

## Testing the Database Connection

Run:

```bash
python3 database_test.py
```

This tests whether Python can connect to PostgreSQL and retrieve job records.

## Future Improvements

- Build a React and TypeScript frontend
- Add an endpoint for updating job status
- Add an endpoint for retrieving one job by ID
- Add better error handling
- Convert database rows into named JSON objects
- Add authentication
- Deploy the application to the cloud