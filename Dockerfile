FROM alpine:3.7
MAINTAINER lukasgarcya@hotmail.com
RUN mkdir -p /opt/djangoSIGE/
WORKDIR /opt/djangoSIGE/
COPY requirements.txt /opt/djangoSIGE/
RUN apk add --no-cache python3 python3-dev \
    py3-cffi zlib-dev gcc jpeg-dev \
    linux-headers libressl-dev \
    libxml2-dev libxslt-dev \
    musl-dev postgresql-dev \
    && pip3 install -r requirements.txt \
    && pip3 install gunicorn psycopg2
