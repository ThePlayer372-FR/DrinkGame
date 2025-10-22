FROM python:3-alpine@sha256:8373231e1e906ddfb457748bfc032c4c06ada8c759b7b62d9c73ec2a3c56e710

RUN apk update

RUN apk add --no-cache \
    build-base \
    python3-dev \
    libffi-dev \
    musl-dev \
    linux-headers

COPY req.txt req.txt

RUN pip install gunicorn eventlet

RUN pip install -r req.txt

COPY src /app

WORKDIR /app

CMD gunicorn -k eventlet -w 1 --bind 0.0.0.0:1337 app:app
