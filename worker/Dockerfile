FROM python:3.9

WORKDIR /DistributedTasksExecutor/worker

COPY worker/requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

COPY worker/*.py .  

CMD ["python", "worker.py"]
