FROM python:3.11.2-slim-bullseye as base

RUN apt-get update -y -qq

WORKDIR /api
COPY . /api

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
