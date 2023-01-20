FROM python:3.10

WORKDIR /backend/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY . .

RUN mkdir -p /backend/django/static/ \
    && mkdir -p /backend/django/media/ \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && groupadd -r web \
    && useradd -r -g web web \
    && chown -R web:web /backend/django


EXPOSE ${DJANGO_PORT}

USER web

ENTRYPOINT gunicorn config.wsgi --worker-class=${GUNICORN_WORKER_CLASS} --workers=${GUNICORN_NUM_WORKERS} --bind 0.0.0.0:${DJANGO_PORT}