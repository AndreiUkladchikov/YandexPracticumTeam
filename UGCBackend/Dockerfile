FROM --platform=linux/amd64 python:3.10.2-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG ru_RU.utf8

RUN useradd -m -s /bin/sh ugcbackend \
     && mkdir -p /home/ugcbackend

WORKDIR /home/ugcbackend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R ugcbackend:ugcbackend /home/ugcbackend \
     && chmod u+x /home/ugcbackend/main.py

USER ugcbackend

ENTRYPOINT gunicorn main:app --workers ${GUNICORN_NUM_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${UGC_BACKEND_PORT}