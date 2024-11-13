FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY data data

CMD echo 'from src import main\n\nmain()' > run.py ; python run.py