import requests
import time
import operator
import re

# Worker configuration
WORKER_NAME = f'worker-{int(time.time())}'
MASTER_URL = 'http://master:5000'

# Define allowed mathematical operations
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def register_worker():
    """Registers the worker with the master."""
    response = requests.post(f'{MASTER_URL}/worker', json={'worker_name': WORKER_NAME})
    print(response.json())

def fetch_task():
    """Continuously fetches and processes tasks from the master."""
    while True:
        response = requests.get(f'{MASTER_URL}/jobs')
        jobs = response.json()

        for job in jobs:
            job_id=job['job_id']
            if not job['finished']:
                tokens=job['task'].split()
                try:
                    result = eval("".join(tokens), {"__builtins__": None}, ops)
                    requests.post(f'{MASTER_URL}/job/{job_id}', json={
                        'finished': True,
                        'answer': result
                    })
                    print(f"Processed job {job_id}: {result}")
                except Exception as e:
                    requests.post(f'{MASTER_URL}/job/{job_id}', json={
                        'finished': True,
                        'answer': f'Error: {str(e)}'
                    })
                    print(f"Error processing job {job_id}: {e}")

        time.sleep(2)  # Prevents excessive requests to the master

if __name__ == '__main__':
    register_worker()
    fetch_task()