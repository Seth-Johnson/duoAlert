FROM python:latest

LABEL Maintainer="SirBomble"

WORKDIR /app
RUN mkdir ./tmp
COPY alert.py ./
COPY phrases.json ./
COPY requirements.txt ./

RUN mkdir ./config
WORKDIR /app/config
COPY config-example.json ./

VOLUME /app/config

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "./alert.py"]