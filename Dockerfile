FROM python:latest

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install pyyaml

RUN pip install sslyze