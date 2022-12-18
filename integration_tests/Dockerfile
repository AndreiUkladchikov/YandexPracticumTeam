FROM --platform=linux/amd64 python:3.10.2-buster

WORKDIR /integration_tests

RUN apt update && apt install -y netcat
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /integration_tests

CMD ["pytest"]