FROM --platform=linux/amd64 python:3.10.2-buster

WORKDIR /fast_api

RUN apt update && apt install -y netcat
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

COPY ./src/main.py /src/main.py

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /fast_api/src

ENTRYPOINT gunicorn main:app --workers ${GUNICORN_NUM_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${BACKEND_PORT}