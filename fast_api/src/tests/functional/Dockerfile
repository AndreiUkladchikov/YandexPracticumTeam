FROM --platform=linux/amd64 python:3.10.2-buster

WORKDIR /functional

RUN apt update && apt install -y netcat
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /functional

ENTRYPOINT [ "/entrypoint.sh" ]