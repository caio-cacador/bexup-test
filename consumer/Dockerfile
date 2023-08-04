FROM python:3.11.2-slim-bullseye as base

RUN apt-get update -y -qq

WORKDIR /
COPY . /.
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
