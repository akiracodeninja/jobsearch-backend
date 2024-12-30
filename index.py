from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from engine import linkedin_job_api, jobs_api, jsearch
import os

load_dotenv()

app = FastAPI()

class JobRequestByLinkedinAPI(BaseModel):
  title: str
  location: str
  limit: int

class JobRequestByJobsAPI(BaseModel):
  title: str
  location: str
  datePosted: str
  nextPage: str

class JobRequestByJSearch(BaseModel):
  query: str
  country: str

# Enable CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post('/linkedin-job-api')
async def get_jobs_by_linkedin_job_api(request: JobRequestByLinkedinAPI):
  title = request.title
  location = request.location
  limit = request.limit

  return linkedin_job_api(title, location, limit)

@app.post('/jobs-api')
async def get_jobs_by_jobs_api(request: JobRequestByJobsAPI):
  title = request.title
  location = request.location
  datePosted = request.datePosted
  nextPage = request.nextPage

  return jobs_api(title, location, datePosted, nextPage)

@app.post('/jsearch')
def get_jobs_by_jsearch(request: JobRequestByJSearch):
  query = request.query
  country = request.country
  
  return jsearch(query, country)

if __name__ == "__main__":
  import uvicorn
  port = int(os.getenv('PORT', 8000))
  uvicorn.run(app, host="0.0.0.0", port=port)