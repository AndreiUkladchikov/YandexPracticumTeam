FROM --platform=linux/amd64 python:3.10.10-slim-bullseye as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG ru_RU.utf8

RUN useradd -m -s /bin/sh promo \
    && mkdir -p /home/promo/web

WORKDIR /home/promo/web

RUN apt-get update && \
    apt-get install --no-install-recommends \
    netcat=1.10-46 dos2unix=7.4.1-1 gettext=0.21-4 -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN find . -type f -print0 | xargs -0 dos2unix 
RUN chown -R promo:promo /home/promo \
    && chmod +x /home/promo/web/*.sh

VOLUME [ "/home/promo/web", ]


FROM base as dev

COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt

USER promo

EXPOSE 8000

ENTRYPOINT ["/home/promo/web/entrypoint.dev.sh"]

FROM base as prod

USER promo

EXPOSE 8000

ENTRYPOINT ["/home/promo/web/entrypoint.prod.sh"]

FROM base as celery-dev

USER promo

ENTRYPOINT ["/home/promo/web/entrypoint.celery.dev.sh"]

FROM base as celery-prod

USER promo

ENTRYPOINT ["/home/promo/web/entrypoint.celery.prod.sh"]

FROM base as celery-beat-prod

USER promo

ENTRYPOINT ["/home/promo/web/entrypoint.celery_beat.prod.sh"]

FROM base as flower-prod

USER promo

ENTRYPOINT ["/home/promo/web/entrypoint.flower.prod.sh"]