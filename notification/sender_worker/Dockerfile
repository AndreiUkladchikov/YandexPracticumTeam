FROM --platform=linux/amd64 python:3.10.2-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG ru_RU.utf8


RUN useradd -m -s /bin/sh sender

WORKDIR /home/sender

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R sender:sender /home/sender \
     && chmod u+x /home/sender/main.py

USER sender
