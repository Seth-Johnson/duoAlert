FROM python:latest
LABEL Maintainer="SirBomble"

RUN mkdir /app
RUN mkdir /app/config
RUN mkdir /app/tmp

WORKDIR /app/config
COPY config/config-example.json ./
COPY config/phrases.json ./

WORKDIR /app
COPY alert.py ./
COPY requirements.txt ./

RUN ls -la config

RUN pip install -r requirements.txt
VOLUME /app/config

CMD [ "python", "./alert.py"]