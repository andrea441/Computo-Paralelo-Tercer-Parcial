# producer/Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir kafka-python oracledb

CMD ["python", "producer.py"]
