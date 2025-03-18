# DistributedTasksExecutor
Distributed tasks executor
Implement a distributed task execution engine in Python, for simple mathematical computations (+-*/). The engine should have 2 active elements - a master process and multiple worker processes. Each worker is responsible of doing a single operation. Both the master and the worker expose a REST API, as follows:
•	master (public API) 
o	POST /submit
This endpoint receives a POST request with a JSON payload in the following form:
{
    "task": "1+(2*3)/4-5"
}
It responds back to the caller with a JSON payload in the following form:
{
    "job_id": 47,
    "finished": false
}
o	GET /job/{id}
This endpoints receives a GET request, with the job_id and returns the status of it as a JSON payload in the following form:
{
    "job_id": 47,
    "finished": true/false,
    "answer": XXX.XXXX or null
}
o	GET /jobs
This endpoint returns a JSON list of the last 100 finished and unfinished jobs
•	master (private API) 
o	POST /worker
This endpoint is used by the workers to announce their presence. Receives a JSON payload in the following form:
{
    "worker_name": "...."
}
•	worker 
o	POST /compute
This endpoint receives a POST request with a JSON payload in the following form:
{
    "operation": "sum/sub/mul/div"
    "op1": XXXX.XXX,
    "op2": XXXX
}
It responds back to the caller with a JSON payload in the following form:
{
    "operation": "sum/sub/mul/div"
    "op1": XXXX.XXX,
    "op2": XXXX,
    "result": XXXX.XXX,
}
The flow for a client of this engine is as follows:
•	assume that an external client wants to compute the result of the "1+(2*3)/4-5" formula
•	the client submits a new task to the master node with the formula and waits for the job_id back.
•	the client then checks once if his job is actually submitted by getting all jobs from the master node and comparing to the received job_id
•	the client will ask every 5 seconds for an individual job if it is finished or not. If yes, print the answer to the console
The flow for the master:
•	the master keeps a record of all the tasks, finished or not
•	the master keeps a record of all available workers
•	when a new task is received, it will save into its record and break it apart into simple operations and distribute them to the workers. Pay attention to the mathematical order of doing operations!
•	when the task is done, it will update the corresponding record with the answer
The flow for worker:
•	as soon as it starts, it will contact the master and announce its presence
•	waits for computation requests and based on their type it will do the corresponding operation and return the answer
Other requirements:
•	the master should be able to be always responsive. This means that it should be able to handle new incoming tasks and processing of already submitted ones in parallel.
•	the system should be able to handle all kind of numeric values, both int and float, both positive and negative values
•	the system should be packaged in 2 docker containers (one for the master and one for the worker) and should be automatized by using docker-compose. With docker-compose you can run multiple workers by scaling it up (hint: --scale parameter of docker-compose)


