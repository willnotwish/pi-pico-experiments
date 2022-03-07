# Running GUI apps in Docker containers

Is it possible?

I found [this article](https://l10nn.medium.com/running-x11-applications-with-docker-75133178d090) relating to X11 apps. I am not 100% sure what they are, but I know X11 is a "windowing system". Hmm, I'm being deliberately vague. See this [SO post](https://unix.stackexchange.com/questions/276168/what-is-x11-exactly).

## First steps

Let's try the example given in the first linked article. I need a `Dockerfile` like this

```
FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y firefox
RUN groupadd -g 1000 nick
RUN useradd -d /home/nick -s /bin/bash -m nick -u 1000 -g 1000
USER nick
ENV HOME /home/nick
CMD /usr/bin/firefox
```

Build it and run it with

```
docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -h $HOSTNAME -v $HOME/.Xauthority:/home/lyonn/.Xauthority gui
```

Presumably this requires X11 to be installed on the host (my PC) because that's what the Docker container will use to draw its GUI. I think this is KDE or GNOME on the host. But I don't really know. Let's see if it works.

It does. Firefox runs fine. It complains about some codecs not being installed when trying to play video, but that's to be expected I guess.

What I want to know is: can I run KiCad with it?

## Installing KiCad

According to the [Ubuntu installation instructions](https://www.kicad.org/download/ubuntu/), you can install KiCad like this

```
sudo add-apt-repository --yes ppa:kicad/kicad-6.0-releases
sudo apt update
sudo apt install --install-recommends kicad
# If you want demo projects
sudo apt install kicad-demos
```

This asked me for the keyboard layout interactively while the Docker image was building. Once I'd answered the question, the process hung.

Instead I modified the `Dockerfile` to install the individual packages and I got it working when I ran it with 
```
docker run -e DISPLAY=$DISPLAY -h $HOSTNAME \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $HOME/.Xauthority:/home/nick/.Xauthority \
  -v $HOME/dev/pi-pico-experiments/kicad-investigation/projects:/home/nick/projects \
  kicad
```

