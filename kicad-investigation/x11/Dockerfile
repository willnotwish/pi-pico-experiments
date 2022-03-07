FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y firefox
RUN groupadd -g 1000 nick
RUN useradd -d /home/nick -s /bin/bash -m nick -u 1000 -g 1000
USER nick
ENV HOME /home/nick
CMD /usr/bin/firefox