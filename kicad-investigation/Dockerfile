FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository --yes ppa:kicad/kicad-6.0-releases
RUN apt-get update
RUN apt-get install --no-install-recommends -y kicad
RUN apt-get install -y kicad-demos kicad-symbols kicad-templates
RUN groupadd -g 1000 nick
RUN useradd -d /home/nick -s /bin/bash -m nick -u 1000 -g 1000
USER nick
ENV HOME /home/nick
CMD kicad