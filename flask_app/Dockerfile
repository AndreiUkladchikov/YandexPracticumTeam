FROM --platform=linux/amd64 python:3.10.2-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./create_roles.py /usr/src/app/create_roles.py
RUN pip install -r requirements.txt --no-cache-dir

COPY . /usr/src/app/