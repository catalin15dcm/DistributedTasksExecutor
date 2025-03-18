from flask import Flask, request, jsonify
import uuid
import sqlite3
import time
import threading
import operator
import re

app = Flask(__name__)

workers= {}

# Define allowed operations
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

DB_FILE = "jobs.db"

def init_db():
    """Create the database and jobs table if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                task TEXT NOT NULL,
                tokens TEXT NOT NULL,
                answer REAL,
                finished BOOLEAN DEFAULT 0
            )
        """)
        conn.commit()

init_db()

def parse_expression(expression):
    """Breaks down an expression into operations and operands based on order of precedence."""
    tokens = re.findall(r'\d+\.?\d*|[+\-*/]', expression)
    return  " ".join(tokens)  # Store as space-separated string

@app.post('/submit')
def submit_task():
    """Accepts a task and stores it in the queue."""
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    job_id = str(uuid.uuid4())
    tokens = parse_expression(data['task'])
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (job_id, task, tokens, finished) VALUES (?, ?, ?, ?)", (job_id, data['task'], tokens, 0))
        conn.commit()
    return jsonify({'job_id': job_id, 'finished': False})

@app.get('/job/<job_id>')
def get_job_status(job_id):
    """Fetch the status and result of a job."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT job_id, finished, answer FROM jobs WHERE job_id = ?", (job_id,))
        job = cursor.fetchone()
    if job:
        return jsonify({'job_id': job[0], 'finished': job[1], 'answer': job[2]})
    return jsonify({'error': 'Job not found'}), 404

@app.post('/job/<job_id>')
def update_job(job_id):
    """Workers send job results back to the master."""
    data = request.get_json()
    if 'finished' not in data or 'answer' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET finished = ?, answer = ? WHERE job_id = ?", (data['finished'], data['answer'], job_id))
        conn.commit()
    return jsonify({'status': 'Job updated', 'job_id': job_id})


@app.get('/jobs')
def get_jobs():
    """Returns the last 100 jobs (both finished and unfinished)."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT job_id, task, finished, answer FROM jobs ORDER BY rowid DESC LIMIT 100")
        jobs = cursor.fetchall()
    return jsonify([{'job_id': job[0], 'task': job[1], 'finished': job[2], 'answer': job[3]} for job in jobs])

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