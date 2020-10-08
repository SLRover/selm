FROM python:3.7-alpine3.9

COPY . /app
WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk add --update tzdata
RUN apk add --no-cache --upgrade bash

ENV FLASK_ENV=production
ENV FLASK_APP=wsgi.py

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app", "-w", "4"]
