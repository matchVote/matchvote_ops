FROM python:3.6.2

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /usr/src
WORKDIR /usr/src

RUN pip install boto3
