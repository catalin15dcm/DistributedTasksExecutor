from flask import Flask, request, jsonify
import uuid
import time
import threading
import operator
import re

app = Flask(__name__)

# Store jobs and workers in memory
jobs = {}
workers = {}
task_queue = []  # Simple in-memory queue

# Define allowed operations
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def parse_expression(expression):
    """Breaks down an expression into operations and operands based on order of precedence."""
    tokens = re.findall(r'\d+\.?\d*|[+\-*/]', expression)
    return tokens

@app.post('/submit')
def submit_task():
    """Accepts a task and stores it in the queue."""
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    job_id = str(uuid.uuid4())
    jobs[job_id] = {'task': data['task'], 'tokens': parse_expression(data['task']), 'finished': False, 'answer': None}
    task_queue.append(job_id)  # Push to in-memory queue
    return jsonify({'job_id': job_id, 'finished': False})

@app.get('/job/<job_id>')
def get_job_status(job_id):
    """Fetch the status and result of a job."""
    job = jobs.get(job_id)
    if job:
        return jsonify({'job_id': job_id, 'finished': job['finished'], 'answer': job['answer']})
    return jsonify({'error': 'Job not found'}), 404

@app.post('/job/<job_id>')
def update_job(job_id):
    """Workers send job results back to the master."""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    data = request.get_json()
    if 'finished' not in data or 'answer' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    jobs[job_id]['finished'] = data['finished']
    jobs[job_id]['answer'] = data['answer']
    
    return jsonify({'status': 'Job updated', 'job_id': job_id})


@app.get('/jobs')
def get_jobs():
    """Returns the last 100 jobs (both finished and unfinished)."""
    return jsonify({'jobs': list(jobs.items())[-100:]})

@app.post('/worker')
def register_worker():
    """Workers register themselves with the master."""
    data = request.get_json()
    if 'worker_name' not in data:
        return jsonify({'error': 'Worker name required'}), 400
    
    workers[data['worker_name']] = time.time()
    return jsonify({'status': 'Worker registered'})

# Background task to remove inactive workers
def monitor_workers():
    while True:
        current_time = time.time()
        for worker in list(workers.keys()):
            if current_time - workers[worker] > 10:
                del workers[worker]
        time.sleep(5)

# Start worker monitoring thread
threading.Thread(target=monitor_workers, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
