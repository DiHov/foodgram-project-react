FROM python:3.7.7-slim

WORKDIR /code
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . ./
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 