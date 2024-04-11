FROM python:3.11

WORKDIR /application

COPY requirements/requirements-dev.txt requirements-dev.txt
COPY requirements/requirements.txt requirements.txt
RUN pip install -r requirements-dev.txt

COPY . .
