FROM --platform=linux/amd64 python:3.9.16-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG ru_RU.utf8

RUN useradd -m -s /bin/sh etlworker \
     && mkdir -p /home/etlworker

WORKDIR /home/etlworker

RUN apt-get update \
     && apt-get install --no-install-recommends \
     tzdata=2021a-1 dos2unix=7.4.1-1 -y \
     && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV TZ="Europe/Moscow"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN find . -type f -print0 | xargs -0 dos2unix \
     && chown -R etlworker:etlworker /home/etlworker \
     && chmod u+x /home/etlworker/entrypoint.sh \
     && chmod u+x /home/etlworker/geventapp.py

USER etlworker

ENTRYPOINT ["/home/etlworker/entrypoint.sh"]