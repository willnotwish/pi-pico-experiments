## Why is my desk LED lamp flickering?

I think it's the power supply. I don't think it's the original unit supplied with the lamp.

I connected a liner PSU (Farnell) to investigate. The central pin on the connector is positive.
The lamp seems to work best at a supply voltage of around 16-17V.

**Aside** I am thinking of combining the desk lamp with the LED strip. The LED strip needs 12V (maybe +-0.5V adjustment).
_Maybe I can design a PSU to power both lamps from a single mains input._

In the end I used an adjustable buck converter connected to the output of an old laptop (I think) PSU
to convert from ~20V to around 16V. I see no flicker. I need to measure the current draw.
