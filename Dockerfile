FROM python:3-alpine

RUN apk update

COPY req.txt req.txt

RUN pip install -r req.txt

COPY src /app

WORKDIR /app

CMD gunicorn -k eventlet -w 1 --bind 0.0.0.0:1337 app:app