FROM python:3.9

WORKDIR /DistributedTasksExecutor/master

COPY master/requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

COPY master/*.py .  

CMD ["python", "master.py"]
