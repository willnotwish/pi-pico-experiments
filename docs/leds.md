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

**Uh oh. There's a problem.** Although the datasheet shows six connectors, the devices I have only have four. Presumably there's a common connection to the three LEDs.

After some tests with my multimeter, I think it's the anodes (+) that are connected together, to the common.

**Or maybe not. They could be completely different: the SK6812 with a controller chip built in. If so, that changes things.**

Here's the [data sheet](https://cdn-shop.adafruit.com/product-files/1138/SK6812+LED+datasheet+.pdf).

To drive one of those requires precise timing: bit banging in a tight loop, or maybe using the SPI.

## Driving SK6812 or similar
Because the driver chip is built in, you don't control red, green and blue separately. You "send" the chip 3x8-bit bytes (one byte per LED). I call this a `triplet`.

As well as power VDD (*i.e.*, 5V) + VSS (0V), the SK6812 has a data input DI. You send the data to DI.

There is also a data output DO, which you can connect to DI of the next LED in the chain if required. To address many LEDs in the chain, you send as many triplets as there are LEDs.

To send a new sequence of triplets, hold the DI line low for at least 50 microseconds.

In this way the data contained within the triplets is clocked to the SK6812 at a fixed frequency `fDIN` of 800kHz.

To send a 0 or a 1 control bit (24 control bits in a triplet), the protocol is

<img width="372" alt="Control waveform" src="https://user-images.githubusercontent.com/52467/126132210-06aef11d-bc76-40f4-b2e7-da1ae47c260d.png">

To send a 0, hold DI high for 300ns (T0H), then low for 900ns (T0L)
To send a 1, hold DI high for 600ns (T1H), then low for 600ns (T1L)

> It takes 1.2us to send either a 1 or a 0. This where the typical fDIN of 800kHz comes from: 1000/1.2 kHz = 833kHz.

There is a large tolerance of +/- 150ns on each of T0H, T0L, T1H and T1L.

There are a few ways to achieve this:
1. Design some dedicated hardware to output the desired but pattern given a 0 or a 1 input.
2. Bit bang one of the Pico's output pins with a software timing loop.
3. Use one of the Pico's coprocessors.

Let's start with option 2 as it's the simplest to understand.

### Bit banging in software

Suppose we only have one LED (SK6812), and we want to "program" it to be red. According to the datasheet, the sequence (I think - it's a bit confusing) is G - R - B.

In binary, for pure red (all bits on), with green & blue turned off, we need

```
0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
```

For a 0, remember, DI high for 300ns, low for 900ns. For a 1, it's DI high for 600ns, low for 600ns.

300ns is the smallest interval we need to consider. Call this one "tick".

Suppose we write an `idle` function that does nothing for a given number of ticks (*i.e.*, multiples of 300ns).

To send a 0, pseudocode would look something like this:

```
set(1)
idle(1)
set(0)
idle(3)
```

Call this `sendOne()`.

For a 1, it's
```
set(1)
idle(2)
set(0)
idle(2)
```

Call this `sendZero()`.

`reset()` holds DI low for at least 50us (the datasheet specifically mentions 80us).

80us is the equivalent of 80000/300 ticks = 267 ticks

`reset` looks like this

```
set(0)
idle(267)
```

To send an 8-bit value `N`, break it down into binary, and then call `sendOne()` or `sendZero()` as appropriate.

For example, to send the decimal value 64 (01000000 in binary):

```
setZero()
setOne()
setZero()
setZero()
setZero()
setZero()
setZero()
setZero()
```

Call this `sendByte(n)`.

To send a triplet, write a function `sendTriplet(red, green, blue)` where `red`, `green` and `blue` are 8 bit values (bytes) between 0 and 255.

**Remember** In the implementation of sendTriplet, the order the SK2812 wants is green-red-blue. So be sure to send the bits in the right order, and not in the order given by the parameter list.

Finally, to address a single LED, first reset and then send the triplet.

To turn the LED red:

```
reset()
sendTriplet(255, 0, 0)
```

For green:
```
reset()
sendTriplet(0, 255, 0)
```

and for blue
```
reset()
sendTriplet(0, 0, 255)
```
__This didn't work. Micropython is too slow. See a more detailed discussion.__

From [a quick investigation](https://github.com/willnotwish/pi-pico-experiments/issues/1) I found that bit banging a GPIO pin in software isn't possible at the kind of speeds we need here, at least not with micropython. The maximum frequency I can achieve is about 65kHz. Too slow, by a long way.

One alternative is to use the SPI.

Another is to follow the guidance in the Pico's C SDK and use PIO instead. This is what did in the end.

## 3.3V vs 5V: level shifting
The SK2812 works at 5V, but the Pico only outputs 3.3V. To be sure this is going to work, we need a level shifter.

Start with a basic NPN transistor as a switch. Note that this will invert the signal. We adjust for this in software: our routines `setOne` and `setZero` need to be transposed.

__This didn't work. A transitor switch is too slow. See a [more detailed discussion](https://github.com/willnotwish/pi-pico-experiments/blob/main/docs/hardware-led-driver.md).__

### More random info
I bought a cheapo LED strip with a solar charger from a discount shop. The LEDs (all white) are not individually addressable. The rechargeable battery is a 1.2V Ni-MH.

I hooked up my scope to look at the driving signal. It's a +/- 2.5V square wave of frequency 4kHz. There must be some sort of boost converter on board. As usual I can't see which chips are used because the manufacturers' markings are scratched off.

![bright-garden-5m-white-led-strip-waveform](https://user-images.githubusercontent.com/52467/128397817-d74e9c1b-0525-4071-966e-92c422cf6e83.png)

