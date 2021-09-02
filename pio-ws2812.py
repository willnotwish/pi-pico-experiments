# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2

# Configure the number of WS2812 LEDs.
NUM_LEDS = 10

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on Pin(6).
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(6))

# Start the StateMachine. It will wait for data on its FIFO.
sm.active(1)

# An array of LEDs
leds = array.array("I", [0 for _ in range(NUM_LEDS)])

# Helper functions
def demo():
    # Cycle colours.
    for i in range(4 * NUM_LEDS):
        for j in range(NUM_LEDS):
            r = j * 100 // (NUM_LEDS - 1)
            b = 100 - j * 100 // (NUM_LEDS - 1)
            if j != i % NUM_LEDS:
                r >>= 3
                b >>= 3
            leds[j] = r << 16 | b
        sm.put(leds, 8)
        time.sleep_ms(50)

    # Fade out.
    for i in range(24):
        for j in range(NUM_LEDS):
            leds[j] >>= 1
        sm.put(leds, 8)
        time.sleep_ms(50)

def display(colours):
    i = 0
    n = len(colours)
    while i < n:
        if i > NUM_LEDS:
            print("Too many colours")
        else:
            leds[i] = colours[i]
        i = i + 1
    print(leds)
    sm.put(leds, 8)
    
def all_off():
    colours = [0 for _ in range(NUM_LEDS)]
    display(colours)

def colour(red, green, blue):
    return (green << 16) + (red << 8) + blue

def pause(ms):
    time.sleep_ms(ms)

# Colour definitions
red = colour(255, 0, 0)
green = colour(0, 100, 0)
blue = colour(0, 0, 255)
white = colour(100, 100, 100)
black = colour(0, 0, 0)
orange = colour(0xff, 0x32, 0x00)
purple = colour(200, 0, 180)

colours = [red, blue, purple, red, green, white, red, green, orange, white]
# colours = [blue, green, red, green, blue, white]

while(1):
    display(colours)
    pause(2000)
    all_off()
    pause(500)


# The main loop
delay = 200
while(0):
    pause(delay)
    display(red)
    pause(delay)
    display(black)

    pause(delay)
    display(white)
    pause(delay)
    display(black)

    pause(delay)
    display(green)
    pause(delay)
    display(black)
    
    pause(delay)
    display(white)
    pause(delay)
    display(black)

    pause(delay)
    display(blue)
    pause(delay)
    display(black)

