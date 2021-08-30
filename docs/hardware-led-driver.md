The problem is that the Pico runs at 3.3V, but the WS2811 LED strip runs at 12V. Even SK2812 LEDs need 5V. Some sort of level translator is required for reliable operation.

I naively thought I could use a regular bipolar transistor as a switch to do the level shifting, feeding it with a 3.3V signal and driving a 12V output. I tried this, and it didn't work at the frequency required (800kHz). The problem (I believe) is the stray (Miller) capacitance combining with load resistance to give a slow rise time.

It's OK when the transistor turns on, but when it turns off the output voltage is so slow to rise that it never gets anywhere near 5V (let alone 12V) by the time it wants to turn back on again. So the signal is messed up.

After investigating a few alternatives, I chose to use a driver chip (the PCA9306 or NCA9306) designed to interface between I2C busses running at different voltages. It will convert from 3.3V to 5V. I think this is a rolls-royce solution. In the future I may try some of the simpler options. However, for now it works fine.

You attach the input side to a 3.3V reference and drive it directly from a Pico PIO pin acting as output. The output side is connected to a 5V supply.

I2C is designed to require an external pull up. I initially tried a 10K pull up resistor, but once again the rise time was poor. When I reduced it to 510R everying was OK. The P/NCA9306 needs its ON current limiting to about 15mA. So in theory you could go as low as 5/15 K (330R). Again, some more experimentation could be carried out here to see what range of resistor values could be used with different types of LED. The higher the value, the less current consumption, but the slower the rise time. However, given that we're going to be driving a whole bunch of LEDs (the strip I have is rated at 45W), the difference in power consumption is largely irrelevant.

I'm going to have a go at drawing a schematic using KiCAD.
