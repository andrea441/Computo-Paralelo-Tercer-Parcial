# web/Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask oracledb

EXPOSE 5000

CMD ["python", "app.py"]