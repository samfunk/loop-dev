FROM python:3.6.3

LABEL maintainer="kirill.sevastyanenko@avant.com"

RUN mkdir -p /root/loop

ADD requirements.txt /root/loop/requirements.txt

RUN pip install --no-cache-dir -r /root/loop/requirements.txt

ADD . /root/loop

EXPOSE 5000

WORKDIR /root/loop

CMD ["gunicorn", "-t", "60", "-b", "0.0.0.0:5000", "app:app"]
