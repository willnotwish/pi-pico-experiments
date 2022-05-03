## Series-parallel LED strip

### Background
I bought a cheapo 5m LED strip from a bargain shop, suitable for low power use, intended to be driven from a small solar panel and a NiMH battery. I decided to repurpose them as an office lamp supplying subdued ambient lighting. Or something.

The 3.1V LEDS were all connected in parallel. I cut the strip into four pieces and wired them in series, meaning that I could drive them from a 12V supply. Each would then drop 3V.

After some investigation I found they were driven by an H bridge at 4kHz.

To dim, alter the pulse width.

[This reference](http://www.da-share.com/circuits/2-wire-led-strings/) has some useful info.

### Driver design
My original idea is to use the RP2040's PIO capabilities to generate two very simple pulse width modulated
control signals. I then added some H bridge hardware using two NPN-PNP transistor pairs.
