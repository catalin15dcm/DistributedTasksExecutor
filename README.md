# DistributedTasksExecutor

## Overview
DistributedTasksExecutor is a Python-based distributed task execution engine designed for simple mathematical computations (`+`, `-`, `*`, `/`). The system consists of two main components:
- **Master Process**: Manages task distribution and execution tracking.
- **Worker Processes**: Perform individual mathematical operations.

Both components expose REST APIs to facilitate interaction and task execution.

## Features
- Supports distributed execution of mathematical computations.
- REST API for task submission and retrieval.
- Automatic worker registration and task assignment.
- Dockerized setup for easy deployment and scalability.

---

## API Endpoints

### Master (Public API)

#### **Submit a Task**
- **Endpoint:** `POST /submit`
- **Request Payload:**
  ```json
  {
      "task": "1+(2*3)/4-5"
  }
  ```
- **Response Payload:**
  ```json
  {
      "job_id": 47,
      "finished": false
  }
  ```

#### **Check Job Status**
- **Endpoint:** `GET /job/{id}`
- **Response Payload:**
  ```json
  {
      "job_id": 47,
      "finished": true/false,
      "answer": XXX.XXXX or null
  }
  ```

#### **Get Recent Jobs**
- **Endpoint:** `GET /jobs`
- **Response Payload:** JSON list of the last 100 jobs (both finished and unfinished).

### Master (Private API)

#### **Worker Registration**
- **Endpoint:** `POST /worker`
- **Request Payload:**
  ```json
  {
      "worker_name": "Worker-1"
  }
  ```

### Worker API

#### **Perform Computation**
- **Endpoint:** `POST /compute`
- **Request Payload:**
  ```json
  {
      "operation": "sum/sub/mul/div",
      "op1": XXXX.XXX,
      "op2": XXXX
  }
  ```
- **Response Payload:**
  ```json
  {
      "operation": "sum/sub/mul/div",
      "op1": XXXX.XXX,
      "op2": XXXX,
      "result": XXXX.XXX
  }
  ```

---

## Workflow

### **Client Workflow**
1. Submit a mathematical formula to the master (`POST /submit`).
2. Receive a `job_id` from the master.
3. Verify that the job is submitted (`GET /jobs`).
4. Periodically check the job status (`GET /job/{id}`) every 5 seconds until completion.
5. Print the final result once available.

### **Master Workflow**
1. Maintain a record of all tasks (finished & unfinished).
2. Track all available workers.
3. When a task is received:
   - Store it.
   - Break it into atomic operations (respecting mathematical order of operations).
   - Assign tasks to available workers.
4. Update task records once computation is complete.

### **Worker Workflow**
1. Announce presence to the master (`POST /worker`).
2. Wait for computation requests.
3. Execute assigned operations and return results.

---

## Requirements
- The master process should always remain responsive, handling new and ongoing tasks in parallel.
- Supports both integers and floating-point numbers (positive & negative values).
- Packaged in two Docker containers:
  - **Master** (Task management & API handling)
  - **Worker** (Computation tasks)
- Uses `docker-compose` for automation and scalability.
- Supports running multiple worker instances via `docker-compose --scale`.

---

## Installation & Deployment
### **Using Docker Compose**
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/DistributedTasksExecutor.git
   cd DistributedTasksExecutor
   ```
2. Build and start the services:
   ```sh
   docker-compose up --build
   ```
3. Scale the worker instances (optional):
   ```sh
   docker-compose up --scale worker=3
   ```
4. The API should now be accessible at `http://localhost:5000`.

---



