import requests
import time
import operator
import socketio
from flask import Flask, request, jsonify
import threading

# Worker configuration
WORKER_NAME = f'worker-{int(time.time())}'
MASTER_URL = 'http://master:5000'

# Define allowed mathematical operations
ops = {
    "sum": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "div": operator.truediv
}
app = Flask(__name__)
sio=socketio.Client()

def register_worker():
    """Registers the worker with the master."""
    response = requests.post(f'{MASTER_URL}/worker', json={'worker_name': WORKER_NAME})
    print(response.json())

@sio.on('new_job')
def process_job(data):
    """Processes a job received from WebSocket."""
    job_id = data['job_id']
    task = data['task']
    print(f"Received job {job_id}, task: {task}")
    try:
        result=eval(task, {"__builtins__": None}, ops)
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


def connect_to_master():
    """Connects to the WebSocket server."""
    print("Connecting to WebSocket server...")
    sio.connect("http://master:5000")  
    print("Connected!")
    sio.wait()

@app.post('/compute')
def compute():
    """Computes a mathematical operation."""
    data = request.get_json()
    if not data or 'operation' not in data or 'op1' not in data or 'op2' not in data:	
        return jsonify({'error': 'Invalid request'}), 400
    
    operation=data['operation']
    op1=data['op1']
    op2=data['op2']
    if operation not in ops:
        return jsonify({'error': 'Invalid operation'}), 400
    
    try:
        result = ops[operation](op1, op2)
        return jsonify({'operation': operation, 'op1': op1, 'op2': op2, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_flask():
    app.run(host="0.0.0.0", port=6000)

if __name__ == '__main__':
    register_worker()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    connect_to_master() 