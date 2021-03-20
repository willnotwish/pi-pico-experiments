## Driving an OLED over SPI

I am interested in repairing an old Pure Evoke Flow DAB whose OLED display stopped working over a year ago. Since then the radio has sat in my shed gathering dust. It is difficult even to turn the radio on with no display. Last time it was on, it worked fine.

Replacement OLEDs for this model are no longer available. I want to replace the original unit with something cheap and cheerful. This is my first foray into driving OLEDs.

The original display is a WINSTAR WEX012864D. The (extremely minimal) datasheet mentions SSD1305. SSD1306 devices of the same resolution (128 x 64) are readily available. I think the two devices are broadly similar: one key difference is to do with a charge pump circuit.

A quick look at the circuit inside the radio shows that the OLED is operating in SPI mode.

My goals are twofold.

1. To understand how to talk to a SSD1306 using SPI. Most of the many examples out there concentrate on I2C, rather than SPI.
2. To get the radio working by replacing the SSD1305-based OLED with a SSD1306.

### Dev environment
For this I used a Raspberry Pi Pico running Micropython.

I started by flashing Micropython onto the pico following the usual instructions.

I set up my development environment using [rshell](https://github.com/dhylands/rshell). It needs Python installed on the host machine, which is in this case my Linux laptop. You could develop on a Raspberry Pi 4 with Thonny, but I wanted to use my laptop with vscode because that's what I use for other (non Python) projects.

I'm trying not to install too much software on my laptop these days; instead I develop in Docker containers. I do so with Rails projects and it works fine.

I wrote a custom Dockerfile based on the official Python image with `rshell` added, launched it with access to the relevant USB device hosting the pico and ran `rshell` from there. I generally use `docker-compose` but you can just do `docker run` if you prefer.

At the `rshell` prompt in vscode you can copy files from the source directories to the pico (the pico appears under the directory `/pyboard` in rshell), enter the `repl` prompt, import modules from the developed code and run sample code to see what happens.

### SPI protocol
I connected a cheap, supposedly-SPI capable OLED to the pico, ran some sample code -- and nothing whatsoever happened! I couldn't get anything to display.

Because I am trying to understand how SPI works, I decided to monitor the SPI hardware on the pico with my Rigol scope. In order to make things as simple as possible I disconnected the OLED and just looked at the SPI clock and data out (that's COPI -- formerly MOSI) lines. They look to be working OK.s


