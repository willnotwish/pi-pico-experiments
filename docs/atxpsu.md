# Background
I have been given a dozen or so power supplies from various unwanted PCs. I think the machines they came from were upgraded over time, so these were surplus to requirements. They are from ~ 2010 I think.

I need 5V for the Pi Pico and 12V for the led strip. The strip I have is rated at 45W. An ATX psu can supply a lot more than that.

# Basics
There are [so many wires](https://en.wikipedia.org/wiki/ATX#Power_supply)! In general though:

```
Red is 5V
Yellow is 12V
Black is ground (0V)
Green is the power on signal (`PS_ON`)
```

There are many articles on the Internet about how to turn your ATX psu into a bench power supply. There are two main things you need to do:

* provide a minimum load of 10W or so
* bring the green `PS_ON` low to start the unit

I used some power resistors salvaged from an old TV as the minimum load.

It's possible to tie `PS_ON` to ground and the unit will start, outputting 5V & 12V as required.

# Ideas

There's also a purple 5V standby (`+5VSB`) wire and a grey "power good" (`PWR_OK`) signal. These are typically used by the motherboard for powering startup circuitry and software.

They could be used as some kind of "soft" startup for my LED display. 
