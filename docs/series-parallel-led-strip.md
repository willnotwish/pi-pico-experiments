## Series-parallel LED strip

### Background
I bought a cheapo 5m LED strip from a bargain shop, suitable for low power use, intended to be driven from a small solar panel and a NiMH battery. I decided to repurpose it as an office lamp supplying subdued ambient lighting. Or something.

The 3.1V LEDS were all connected in parallel. I cut the strip into four pieces and wired them in series, meaning that I could drive them from a 12V supply. Each would then drop 3V.

After some investigation I found they were driven by an H bridge at 4kHz.

To dim, alter the pulse width.

[This reference](http://www.da-share.com/circuits/2-wire-led-strings/) has some useful info.

### Driver design
My original idea is to use the RP2040's PIO capabilities to generate two very simple pulse width modulated
control signals. I then added some H bridge hardware using two NPN-PNP transistor pairs.

At first, with 10K base resistors, there wasn't enough base current to drive the transistors into saturation. Once I reduced the resistance to 1K, the strip seemed quite bright.

Current consumption from the 12V supply is approximately 180mA, which seems quite low. About 2.2W.

### Still to do
1. Figure out how to power the whole thing from one supply.
2. Implement the hardware logic to prevent both legs of the H bridge turning on at the same time and short-circuiting the driver transistors.
3. Investigate dimming options.

### Power supply
Currently 12V comes from an old SMPS and the Pico is powered over USB. I need to look at various options for supplying the Pico from the 12V supply.

### Protective logic
I have a design somewhere

### Dimming control
- pushbuttons
- 10-turn pot
- old-skool pot

I know how to vary the pulse width in a loop, so I just need to work out how to scan buttons or use a potentiometer. The RP2040 chip has an A/D converter built in.
