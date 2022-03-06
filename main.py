# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2

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

class LedStrip:
    def __init__(self, id, pin_number, num_leds):
        self.sm = rp2.StateMachine(id, ws2812, freq=8_000_000, sideset_base=Pin(pin_number))
        self.sm.active(1)
        self.count = num_leds
        self.leds = array.array("I", [0 for _ in range(num_leds)])

    def display(self, triplets):
        n = len(triplets)
        if n > self.count:
            raise Exception("Too much data to display! You have {} LEDs but you tried to display {} triplets".format(self.count, n))
        
        i = 0
        while i < n:
            self.leds[i] = triplets[i]
            i = i + 1
    
        print("Triplets to display (decimal): {}".format(triplets))
        print("Triplets to display (hex): [{}]".format(', '.join(hex(x) for x in triplets)))
        
        self.sm.put(self.leds, 8)
        
    def off(self):
        zeroes = [0 for _ in range(self.count)]
        self.display(zeroes)
        
    def demo(self):
        n = self.count
        
        # Cycle colours.
        for i in range(4 * n):
            for j in range(n):
                r = j * 100 // (n - 1)
                b = 100 - j * 100 // (n - 1)
                if j != i % n:
                    r >>= 3
                    b >>= 3
                self.leds[j] = r << 16 | b
            self.sm.put(self.leds, 8)
            time.sleep_ms(50)

        # Fade out.
        for i in range(24):
            for j in range(n):
                self.leds[j] >>= 1
            self.sm.put(self.leds, 8)
            time.sleep_ms(50)

internal_leds = LedStrip(0, 6, 10)
external_leds = LedStrip(1, 7, 50)


def colour(red, green, blue):
    return (green << 16) + (red << 8) + blue

def pause(ms):
    time.sleep_ms(ms)

# Colour definitions
red    = colour(255, 0, 0)
green  = colour(0, 255, 0)
blue   = colour(0, 0, 255)
white  = colour(255, 255, 255)
black  = colour(0, 0, 0)
orange = colour(0xff, 0x32, 0x00)
purple = colour(200, 0, 180)

print('Part 1: Starting up')
pause(1000)
internal_leds.display([white, black, black, black, black, black, black, black, black, black])
pause(10)
internal_leds.display([black, white, black, black, black, black, black, black, black, black])
pause(10)
internal_leds.display([black, black, white, black, black, black, black, black, black, black])
pause(10)
internal_leds.display([black, black, black, white, black, black, black, black, black, black])
pause(10)
internal_leds.display([black, black, black, black, white, black, black, black, black, black])
pause(10)
internal_leds.display([black, black, black, black, black, white, black, black, black, black])
pause(10)
internal_leds.display([black, black, black, black, black, black, white, black, black, black])
pause(10)
internal_leds.display([black, black, black, black, black, black, black, white, black, black])
pause(10)
internal_leds.display([black, black, black, black, black, black, black, black, white, black])
pause(10)
internal_leds.display([black, black, black, black, black, black, black, black, black, white])
pause(10)
#internal_leds.off()


colours = [black for _ in range(10)]
internal_leds.display(colours)
pause(1000)

for place in range(10):
    print("Place is {}".format(place))
    
    if place == 0:
        colours[place] = white
#    elif place == 9:
#        colours[place] = white
    else:
        colours[place-1] = black
        colours[place] = white
        
    internal_leds.display(colours)
    pause(1000)
    



#place = 0
#print("Place is {}".format(place))

#colours[place] = white
#internal_leds.display(colours)
#pause(1000)

#colours[place] = black
#colours[place+1] = white
#internal_leds.display(colours)
#pause(1000)

#place = place + 1
#print("Place is {}".format(place))
#colours[place] = black
#colours[place+1] = white
#internal_leds.display(colours)
pause(1000)

internal_leds.off()



print('Decent!')



#ten_reds     = [red    for _ in range(10)]
#ten_greens   = [green  for _ in range(10)]
#ten_blues    = [blue   for _ in range(10)]
#fifty_greens = [green  for _ in range(50)]
#ten_whites   = [white  for _ in range(10)]
#ten_oranges  = [orange for _ in range(10)]

#internal_leds.display(ten_oranges)
#pause(2000)
#external_leds.demo()
#internal_leds.off()
#pause(2000)

#pause(2000)
#internal_leds.display([white, black, black, black, black, black, black, black, black, black])
#pause(2000)
#internal_leds.display([black, white, black, black, black, black, black, black, black, black])
#pause(2000)
#internal_leds.display([black, black, white, black, black, black, black, black, black, black])
#pause(2000)
#internal_leds.off()
#pause(2000)

#triplets = [black for _ in range(10)]

#internal_leds.display(triplets)
#pause(2000)
#print("Starting")



#triplets[0] = white
#internal_leds.display(triplets)
#pause(2000)
    
#triplets[0] = black
#triplets[1] = white
#internal_leds.display(triplets)
#pause(2000)

#triplets[1] = black
#triplets[2] = white
#internal_leds.display(triplets)
#pause(2000)

#triplets[2] = black
#triplets[3] = white
#internal_leds.display(triplets)
#pause(2000)

#triplets[3] = black
#triplets[4] = white
#internal_leds.display(triplets)
#pause(2000)

#triplets[4] = black
#triplets[5] = white
#internal_leds.display(triplets)
#pause(2000)

#internal_leds.off()
