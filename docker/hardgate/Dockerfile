FROM python:3.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --root-user-action=ignore -U pip

COPY ./requirements.txt .

COPY ./app.py .

COPY ./.env .

RUN pip install --root-user-action=ignore -r requirements.txt

RUN apk add wireguard-tools curl

EXPOSE 5050

