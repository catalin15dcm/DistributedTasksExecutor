import requests
import time

# Master API URL
MASTER_URL = "http://localhost:5000"

def submit_task(task):
    """Submits a mathematical expression to the master."""
    response = requests.post(f"{MASTER_URL}/submit", json={"task": task})
    
    if response.status_code == 200:
        job_id = response.json()["job_id"]
        print(f"Task submitted successfully! Job ID: {job_id}")
        return job_id
    else:
        print(f"Error submitting task: {response.text}")
        return None

def check_job_submission(job_id):
    """Checks if the submitted job exists in the job list."""
    response = requests.get(f"{MASTER_URL}/jobs")
    
    if response.status_code == 200:
        jobs = response.json()  #

        if any(job["job_id"] == job_id for job in jobs):
            print(f"Job {job_id} found in job list!")
        else:
            print(f"Job {job_id} NOT found in job list!")
    else:
        print(f"Error retrieving job list: {response.text}")


def poll_job_status(job_id):
    """Polls the job status every 5 seconds until completion."""
    print(f"Checking job status for Job ID: {job_id}...")
    
    while True:
        response = requests.get(f"{MASTER_URL}/job/{job_id}")
        
        if response.status_code == 200:
            job_data = response.json()
            
            if job_data["finished"]:
                print(f"Job completed! Result: {job_data['answer']}")
                break
            else:
                print("Job is still in progress, checking again in 5 seconds...")
        else:
            print(f"Error retrieving job status: {response.text}")
        
        time.sleep(5)

if __name__ == "__main__":
    
    tasks = [
    "1+(2*3)/4-5",
    "10-3*2",
    "(8+2)/5",
    "7*3-4",
    "5+(6/2)-9"
]
    for task in tasks:
        job_id = submit_task(task)

        if job_id:
        
            check_job_submission(job_id)

            poll_job_status(job_id)


