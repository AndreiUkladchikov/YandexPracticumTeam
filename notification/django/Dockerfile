FROM --platform=linux/amd64 python:3.10.2-buster

ENV PYTHONUNBUFFERD=1

WORKDIR /admin_panel

RUN apt update && apt install -y netcat
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

# dev settings for fast start
#COPY ./entrypoint-dev.sh /entrypoint.sh

COPY ./entrypoint.sh /entrypoint.sh

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["/entrypoint.sh"]
