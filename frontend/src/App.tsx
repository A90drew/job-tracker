import './App.css'
import { useEffect, useState } from 'react'

interface Job { 
  id: number
  role: string
  company: string
  status: string
  posted: string | null
  deadline: string
  url: string | null
} 

function App() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [role, setRole] = useState("")
  const [company, setCompany] = useState("")
  const [deadline, setDeadline] = useState("")
  const [loading, setLoading] = useState(true)
  const [selectedStatus, setSelectedStatus] = useState("All")
  const [url, setUrl] = useState("")
  const today = new Date()
  const twoWeeksFromNow = new Date()
  twoWeeksFromNow.setDate(today.getDate()+14)
  const filteredJobs =
  selectedStatus === "All"
    ? jobs
    : selectedStatus === "Upcoming"
      ? jobs.filter((job) => {
          const deadline = new Date(job.deadline)

          return deadline >= today && deadline <= twoWeeksFromNow
        })
      : jobs.filter((job) => job.status === selectedStatus)
  const [sortOption, setSortOption] = useState("deadline")
  const sortedJobs = [...filteredJobs].sort((a, b) => {
  if (sortOption === "deadline") {
    return new Date(a.deadline).getTime() - new Date(b.deadline).getTime()
  }

  if (sortOption === "role") {
    return a.role.localeCompare(b.role)
  }

  if (sortOption === "company") {
    return a.company.localeCompare(b.company)
  }

  if (sortOption === "status") {
    return a.status.localeCompare(b.status)
  }

  return 0
})
const [selectedJob, setSelectedJob] = useState<Job | null>(null)

  function loadJobs(){
    fetch("http://127.0.0.1:8000/jobs")
    .then((response) => response.json())
    .then((data) => {
      setJobs(data)
    })
    .finally(() => {
      setLoading(false)
    })
  }
  useEffect (() => {
    loadJobs()
  }, [])

function updateStatus(jobId: number, newStatus: string) {
  fetch(`http://127.0.0.1:8000/jobs/${jobId}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      status: newStatus
    })
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to update status")
      }

      return response.json()
    })
    .then(() => {
      loadJobs()
      alert("Status updated!")
    })
    .catch((error) => {
      alert(error.message)
    })
}

function deleteJob(jobId: number) {
fetch(`http://127.0.0.1:8000/jobs/${jobId}`, {
    method: "DELETE"
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to delete job")
      }

      return response.json()
    })
    .then(() => {
      loadJobs()
      alert("Job deleted!")
    })
    .catch((error) => {
      alert(error.message)
    })
}

  return (
    <main>
      <h1>Job Application Tracker</h1>
      {selectedJob && (
        <section className="job-details">
          <h2>{selectedJob.role}</h2>
          <p>Company: {selectedJob.company}</p>
          <p>Status: {selectedJob.status}</p>
          <p>Deadline: {selectedJob.deadline}</p>
          {selectedJob.url ? (
            <a
              href={selectedJob.url}
              target="_blank"
              rel="noreferrer"
            >
              View job posting
            </a>
          ) : (
            <p>No job posting link available.</p>
          )}
          <button
            type="button"
            onClick={() => setSelectedJob(null)}
          >
            Back to jobs
          </button>
        </section>
      )}
      {!selectedJob &&(
        <>
      <section className="dashboard">
        <h2>Dashboard</h2>
        <div className="dashboard-cards">
          <div className="summary-card"
          onClick={() => setSelectedStatus("All")}>
            <h3>Total jobs</h3>
            <p>{jobs.length}</p>
            </div>

            <div className="summary-card"
            onClick={() => setSelectedStatus("Not submitted")}>
              <h3>Not Submitted</h3>
              <p>{jobs.filter((job) => job.status === "Not submitted").length}</p>
            </div>

            <div className="summary-card"
            onClick={() => setSelectedStatus("Submitted")}>
              <h3>Submitted</h3>
              <p>{jobs.filter((job) => job.status === "Submitted").length}</p>
            </div>

            <div className="summary-card"
            onClick={() => setSelectedStatus("Interview")}>
              <h3>Interviews</h3>
              <p>{jobs.filter((job) => job.status === "Interview").length}</p>
            </div>

            <div className="summary-card"
            onClick={() => setSelectedStatus("Upcoming")}>
                <h3>Upcoming</h3>
                <p>
                  {jobs.filter((job) => {
                    const deadline = new Date(job.deadline)

                    return deadline >= today && deadline <= twoWeeksFromNow
                  }).length}
                </p>
              </div>
        </div>
      </section>
      <label className="sort-control">
        Sort by:
        <select
        value={sortOption}
        onChange={(event) => setSortOption(event.target.value)}
        >
          <option value="deadline">Deadline</option>
          <option value="role">Role</option>
          <option value="company">Company</option>
        </select>
      </label>
      <form className="job-form"
        onSubmit={(event) => {
          event.preventDefault()
          const newJob = {
            role,
            company,
            deadline,
            url
          }
          fetch("http://127.0.0.1:8000/jobs", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(newJob)
          })
          .then(async (response) => {
            if (!response.ok) {
              const errorDetails = await response.text()
              throw new Error(
                `Request failed with status ${response.status}: ${errorDetails}`
              )
            }
            return response.json()
          })
          .then(() => {
            loadJobs()

            setRole("")
            setCompany("")
            setDeadline("")
            setUrl("")

            alert("Job was added successfully!")
          })
          .catch((error) => {
            alert(error.message)
          })
        }
      }
      >
        {
          <input
          value={role}
          onChange={(event) => setRole(event.target.value)}
          placeholder="Job role"
          required
          />
          }
        {
          <input
          value={company}
          onChange={(event) => setCompany(event.target.value)}
          placeholder="Company name"
          required
          />
          }
        {
          <input
          type="date"
          value={deadline}
          onChange={(event) => setDeadline(event.target.value)}
          required
          />
          }
        {
          <input
          type="url"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          placeholder="Job posting URL"
          required
          />
          }
        <button type="submit">Add Job</button>
      </form>
      {loading && <p>Loading jobs...</p>}
      {!loading && sortedJobs.length === 0 && (
        <p>No jobs found for this view.</p>
        )}
      {!loading && sortedJobs.map((job) => (
        <div className={`job-card status-${job.status
          .toLowerCase()
          .replace(" ", "-")}`}
        key={job.id}
        onClick={() => setSelectedJob(job)}
        >
          <h2>{job.role}</h2>
          <p>Company: {job.company}</p>
          <p>Status: {job.status}</p>
          <p>Deadline: {job.deadline}</p>

          <select
          value={job.status}
          onChange={(event) =>
            updateStatus(job.id, event.target.value)
          }
          >
            <option value="Not submitted">Not submitted</option>
            <option value="Submitted">Submitted</option>
            <option value="Interview">Interview</option>
            <option value="Rejected">Rejected</option>
            <option value="Accepted">Accepted</option>
          </select>
          <button
          type="button"
          onClick={() => {
            const confirmed = window.confirm(
            "Are you sure you want to delete this job?"
          )

          if (confirmed) {
            deleteJob(job.id)
          }
        }}
      >
        Delete
      </button>
        </div>
      ))}
      </>
      )}
    </main>
  )
}

export default App