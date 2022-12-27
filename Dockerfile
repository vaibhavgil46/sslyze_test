FROM python:latest

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --upgrade sslyze pyyaml

ENV DOMAIN -h
ENV MAIL -h

COPY ./sslyze_api.py ./
ENV TYPE --yaml

CMD [ "sh", "-c", "python3 ./sslyze_api.py $DOMAIN $MAIL $TYPE" ]
