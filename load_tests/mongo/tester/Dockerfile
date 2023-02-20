FROM --platform=linux/amd64 python:3.11.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -m -s /bin/sh mongotest \
     && mkdir -p /home/mongotest

WORKDIR /home/mongotest

RUN apt-get update \
     && apt-get install --no-install-recommends \
     dos2unix=7.4.1-1 -y \
     && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN find . -type f -print0 | xargs -0 dos2unix \
     && chown -R mongotest:mongotest /home/mongotest \
     && chmod u+x /home/mongotest/configure.sh \
     && chmod u+x /home/mongotest/main.py

USER mongotest

ENTRYPOINT ["/home/mongotest/configure.sh"]
