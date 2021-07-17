## 5050 LEDs

I have a bunch of these RGB LEDs to experiment with.

They are SMD devices, with 6 pins. A bit tricky to solder, maybe.

<img width="746" alt="Screenshot 2021-07-17 at 18 57 00" src="https://user-images.githubusercontent.com/52467/126045895-335d9f15-20b2-4dec-a5d8-697624fa306c.png">

The datasheet doesn't say which colour is which pin pair, as far as I can tell.

Also, the red LED is different from the other two, in terms of electrical characteristics. For red, forward voltage should be in the range 1.8 - 2.4V (mean: 2.1). For G & B it's 2.8 - 3.6V (mean: 3.2).

20mA is the maximum current: keep it a bit below this at first.

Assume a 5V supply, and a drop across the red diode of 2.1V. At 20mA (max), R (min) = (5 - 2.1)/20 K = 145 ohm.
For the green and blue LEDs, the average voltage is 3.2V, so we only need R (min) = (5 - 3.2)/20 K = 90 ohm.

To test which pin is which, be conservative. Try a 220 R resistor.

If this works, we could go for R(red) = 150 R, and R (green/blue) = 100 R.

Uh oh. There's a problem. Although the datasheet shows six connectors, the devices I have only have four. Presumably there's a common connection to the three LEDs.

After some tests with my multimeter, I think it's the anodes (+) that are connected together.

