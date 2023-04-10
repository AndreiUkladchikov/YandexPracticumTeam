FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/conf.d/default.conf /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY app.conf /etc/nginx/conf.d/app.conf
RUN mkdir -p /data/log
