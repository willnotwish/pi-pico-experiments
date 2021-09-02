I previously found out that bit banging [is not possible](https://github.com/willnotwish/pi-pico-experiments/issues/1) at the speeds the LED strip requires (800kHz).

It turns out that the Pico has a much better way of handling something like this: programmable input/output or PIO. It's really quite a clever idea that the RPi2040 designers have included in their microcontroller. It's like having a very limited, very simple coprocessor on the chip that can do the simplest thing really well. PIOs (there are two I think) are documented in the Rpi2040 data sheet. There's an example for driving WS2812 LEDs!

I followed the C example first and it worked fine. I then discovered that Micropython can do the same as well. Fantastic!
