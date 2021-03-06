FROM ubuntu:16.10

RUN apt-get update -y && apt-get install -yq wget build-essential gcc zlib1g-dev

WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz \
        && tar zxf Python-3.6.0.tgz \
        && cd Python-3.6.0 \
        && ./configure \
        && make altinstall
ENV PYTHONIOENCODING "utf-8"

WORKDIR /

