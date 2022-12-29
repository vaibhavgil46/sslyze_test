FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --upgrade -r requirements.txt

COPY ./libary/* /app/libary/

ENV DOMAIN -h 
ENV EMAIL -h

COPY ./main.py ./
ENV TYPE --yaml

CMD [ "sh", "-c", "python3 ./main.py -e DOMAIN=$DOMAIN -e EMAIL=$EMAIL -e TYPE=$TYPE" ]
