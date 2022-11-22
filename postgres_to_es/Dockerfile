FROM --platform=linux/amd64 python:3.10.2-buster

WORKDIR /postgres_to_es

RUN apt update && apt install -y netcat
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

COPY ./state.json /state.json
COPY ./main.py /main.py

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python", "main.py"]
