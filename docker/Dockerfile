FROM python:3.5.5-alpine
MAINTAINER chie hayashida<chie8842@gmail.com>

RUN apk update \
    && apk add sqlite \
    && apk add socat \
    && apk add git

RUN pip install pytest

WORKDIR /tmp/work

