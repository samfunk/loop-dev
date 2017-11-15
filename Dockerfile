FROM python:3.6.3

LABEL maintainer="kirill.sevastyanenko@avant.com"

RUN mkdir -p /root/loop

ADD . /root/loop

RUN pip install --no-cache-dir -r /root/loop/requirements.txt

EXPOSE 5000

WORKDIR /root/loop
