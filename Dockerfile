FROM python:alpine

WORKDIR /app
RUN pip install --upgrade pip setuptools wheel && \
    pip install --upgrade sslyze pyyaml
