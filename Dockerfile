FROM ubuntu:19.10

MAINTAINER Vaclav Sisl <vaclav.sisl@gmail.com>

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip git

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./ /Covid19_cz_districts
WORKDIR /Covid19_cz_districts

CMD gunicorn --bind 0.0.0.0:80 --workers=4 wsgi