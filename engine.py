import requests
from dotenv import load_dotenv
import logging
import json
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

def get_api_key(index=0):
  api_key = [
    '8fd174f370msh36926178470c8d5p1bb8b0jsn5326dfe242ba'
  ]
  
  return api_key[index]

def save_result_to_file(data, filename):
  parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
  file_path = os.path.join(parent_dir, filename)
  with open(file_path, 'w') as file:
      json.dump(data, file, indent=4)
  logger.info(f"Result saved to {file_path}")

def get_data_from_raw(raw_data, type=0):
  if isinstance(raw_data, list):
    processed_data = []
    for item in raw_data:
      if (type == 0):
        data = {
          'date': item['date_posted'],
          'type': item['employment_type'],
          'title': item['title'],
          'url': item['url'],
          'location': item['locations_derived'],
          'company': item['linkedin_org_url']
        }
        processed_data.append(data)
      elif (type == 1):
        job_providers = item['jobProviders']
        providers = []
        for provider in job_providers:
            providers.append({
              'site': provider['jobProvider'],
              'url': provider['url']
            })

        data = {
          'date': item['timeAgoPosted'],
          'type': item['employmentType'],
          'title': item['title'],
          'url': providers,
          'location': item['location'],
          'company': item['company']
        }
        processed_data.append(data)
      else:
        data = {
          'date': raw_data['job_posted_at_datetime_utc'],
          'type': item['job_employment_types'][0],
          'title': item['job_title'],
          'url': {
              'linkedin': item['job_apply_link'],
              'google': item['job_google_link']
          },
          'location': item['job_country'] + ', ' + item['job_location'],
          'company': item['company']
        }
        processed_data.append(data)

    return processed_data
  else:
    return None
def linkedin_job_api(title="full stack", location = "United States", limit = 10):
  url = "https://linkedin-jobs-api2.p.rapidapi.com/active-jb-7d"
  querystring = {
    "title_filter": title,
    "location_filter": location,
    "remote":"true",
    "limit": limit
  }

  headers = {
    "x-rapidapi-key": get_api_key(),
    "x-rapidapi-host": "linkedin-jobs-api2.p.rapidapi.com"
  }

  try:
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    result = response.json()

    data = get_data_from_raw(result)
    save_result_to_file(data, 'linkedin_jobs.json')
    return result
  except requests.exceptions.RequestException as e:
    logger.error(f"HTTP Request for Linkedin Job Api failed: {e}")
    return None

def jobs_api(title="Web Developer", location="United States", datePosted="week", nextPage=""):
  url = "https://jobs-api14.p.rapidapi.com/v2/list"
  querystring = {
    "query": title,
    "location": location,
    "autoTranslateLocation":"true",
    "remoteOnly":"true",
    "employmentTypes":"fulltime;parttime;contractor",
    "datePosted":datePosted,
    "nextPage": nextPage
  }

  headers = {
    "x-rapidapi-key": get_api_key(),
    "x-rapidapi-host": "jobs-api14.p.rapidapi.com"
  }

  try:
      response = requests.get(url, headers=headers, params=querystring)
      response.raise_for_status()
      return response.json()
  except requests.exceptions.RequestException as e:
      logger.error(f"HTTP Request for Jobs Api failed: {e}")
      return None

def jsearch(query, country):
  url = "https://jsearch.p.rapidapi.com/search"
  querystring = {
    "query": query,
    "page":"1",
    "num_pages":"10",
    "country": country,
    "date_posted":"3days"
  }

  headers = {
    "x-rapidapi-key": get_api_key(),
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
  }

  try:
      response = requests.get(url, headers=headers, params=querystring)
      response.raise_for_status()
      return response.json()
  except requests.exceptions.RequestException as e:
      logger.error(f"HTTP Request for JSearch failed: {e}")
      return None