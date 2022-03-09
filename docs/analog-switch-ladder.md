# Detecting push button presses using a voltage divider

I have a front panel PCB from an old car stereo (ex Mitsubishi - mid 2000s).

It has plenty of good quality pushbutton switches, each connected via a different value resistor to a common point.
I think the idea is to form a voltage divider. By measuring the
resulting DC voltage using the A/D converter on the RP2040 I can tell which switch was pressed.

This makes a simple low cost switching multiplexer.

Here's the panel.

![panel](/home/nick/dev/pi-pico-experiments/docs/images/panel.png)

The switches labelled 701 to 707 are wired something like this:
> cct diagram here

I measured the resistances as follows:

| Switch label | R    |
|--------------|------|
| 701          | 820R |
| 702          | +1K2 |
| 703          | +1K2 |
| 704          | +1K5 |
| 705          | +1K8 |
| 706          | +2K2 |
| 707          | +2K7 |

When SW701 is pressed, the effective resistance R1 = 820Ω.

**Note the resistance is cumulative**, indicated by the plus (+) sign in the table above. 
When SW702 is clicked, R2 = 820R + 1K2 = 820 + 1200 = 2020Ω.

If the ADC sample is 65535 at 3.3V (maximum sample voltage "FSD") then we have something like this:

| Switch |        Resistor value Ω          | Effective R   | 1K0        | Value      | 3K3        | Value      | 10K        | Value      |
|--------|------------------|---------------|------------|------------|------------|------------|------------|------------|
| 701    | 820              | 820           | 0.451      | 29527      | 0.199      | 13043      | 0.076      | 4967       |
| 702    | 1200             | 2020          | 0.669      | 43835      | 0.380      | 24884      | 0.168      | 11013      |
| 703    | 1200             | 3220          | 0.763      | 50005      | 0.494      | 32365      | 0.244      | 15962      |
| 704    | 1500             | 4720          | 0.825      | 54078      | 0.589      | 38569      | 0.321      | 21014      |
| 705    | 1800             | 6520          | 0.867      | 56820      | 0.664      | 43512      | 0.395      | 25865      |
| 706    | 2200             | 8720          | 0.897      | 58793      | 0.725      | 47543      | 0.466      | 30527      |
| 707    | 2700             | 11420         | 0.919      | 60258      | 0.776      | 50843      | 0.533      | 34940      |

Putting a 1K series resistor and connecting the high side to 3.3V should yield the sampled values in the 1K0 column. 
On the other hand, a 10K series resistor yields the values in the last column.

Whichever resistor is chosen, a set of "switch identification" band needs to be defined.

## Definitions

An identification band may have a lower limit and an upper limit; either is optional, but there must be one or the other
(or both).

A _switch identifier_ has a number of identification bands: one per switch. Each band identifies a switch. 
To find out which switch has been pressed, take a sample and work out in which band it lies.

Assuming a 10K series resistor, here are the (theoretical) bands.

| Series R Ω | Multiplier |      | min   | max   |
|------------|------------|------|-------|-------|
| 10000      |            |      |       |       |
| 0.076      | 4967       | 4967 |       | 7990  |
| 0.168      | 11013      | 6047 | 7990  | 13488 |
| 0.244      | 15962      | 4949 | 13488 | 18488 |
| 0.321      | 21014      | 5052 | 18488 | 23439 |
| 0.395      | 25865      | 4851 | 23439 | 28196 |
| 0.466      | 30527      | 4662 | 28196 | 32733 |
| 0.533      | 34940      | 4413 | 32733 |       |

Because bands cannot overlap, they can be defined more succinctly as a series of breakpoints:
- B1: 7990
- B2: 13488
- B3: 18488
- B4: 23439
- B5: 28196
- B6: 32733

Below B1, SW701 was pressed. Above B6, it must have been SW707. Between B1 & B2, it's SW702. And so on.
