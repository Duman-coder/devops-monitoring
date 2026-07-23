FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ping_check.py .
COPY hosts.txt .

ENV CHECK_INTERVAL=60

CMD ["python3", "ping_check.py"]
