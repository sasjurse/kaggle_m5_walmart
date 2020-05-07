# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
FROM python:3.7-buster as libraries

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

FROM libraries
COPY . /app
WORKDIR /app
