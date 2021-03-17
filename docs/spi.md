## Driving an OLED over SPI

I am interested in repairing an old Pure Evoke Flow DAB whose OLED display stopped working over a year ago. Since then the radio has sat in my shed gathering dust. It is difficult even to turn the radio on with no display. Last time it was on, it worked fine.

Replacement OLEDs for this model are no longer available. I want to replace the original unit with something cheap and cheerful. This is my first foray into driving OLEDs.

The original display is a WINSTAR WEX012864D. The (extremely minimal) datasheet mentions SSD1305. SSD1306 devices of the same resolution (128 x 64) are readily available. I think the two devices are broadly similar: one key difference is to do with a charge pump circuit.

A quick look at the circuit inside the radio shows that the OLED is operating in SPI mode.

My goals are twofold.

1. To understand how to talk to a SSD1306 using SPI. Most of the many examples out there concentrate on I2C, rather than SPI.
2. To get the radio working by replacing the SSD1305-based OLED with a SSD1306.

### SPI interfacing experiments
For this I used a Raspberry Pi Pico running Micropython.
