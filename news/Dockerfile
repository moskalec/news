FROM python:3.9.12-alpine

WORKDIR /usr/src/news

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY . .meta/packages ./
RUN pip install -r .meta/packages

COPY . .