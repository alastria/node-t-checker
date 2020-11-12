FROM python:3.8-slim

ARG REPOSITORY
ARG TRAVIS_PULL_REQUEST
ARG ENODE_URL
ARG ENODE_USERNAME
ARG ENODE_PASSWORD
ARG ENODE_DB

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV REPOSITORY=$REPOSITORY
ENV GITHUB_TOKEN=$GITHUB_TOKEN
ENV TRAVIS_PULL_REQUEST=$TRAVIS_PULL_REQUEST
ENV ENODE_URL=$ENODE_URL
ENV ENODE_USERNAME=$ENODE_USERNAME
ENV ENODE_PASSWORD=$ENODE_PASSWORD
ENV ENODE_DB=$ENODE_DB

RUN mkdir /code

WORKDIR /code

RUN apt -y update && apt install -y whois nmap
RUN pip install 'poetry==1.0.5'
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

CMD ["poetry", "run", "validator/main.py"]
