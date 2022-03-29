# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.15

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN apk add --no-cache git zlib-dev jpeg-dev musl-dev gcc

RUN pip3 install -U -r requirements.txt

COPY /bot .

CMD [ "python3.10", "main.py" ]
