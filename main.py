# from machine import ADC, Pin

from switch.detect import Detector
from switch.switch import Switch

import machine
import time

detector0 = Detector([
    Switch('SW701', 7990),
    Switch('SW702', 13488),
    Switch('SW703', 18488),
    Switch('SW704', 23439),
    Switch('SW705', 28196),
    Switch('SW706', 32733),
    Switch('SW707', 36000),
    Switch('SW708', 41000),
    Switch('SW709', 44000),
    Switch('SW710', 48000),
    Switch('SW711', 51000)
], machine.ADC(machine.Pin(26))
)

detector1 = Detector([
    Switch('SW712', 7990),
    Switch('SW713', 13488),
    Switch('SW714', 18488),
    Switch('SW715', 23439),
    Switch('SW716', 28196),
], machine.ADC(machine.Pin(27))
)

switch0 = None
switch1 = None

# ISR
def detect_isr(timer):
    global switch0
    global switch1

    switch = detector0.detect()
    if switch is not None and switch != switch0:
        switch0 = switch

    switch = detector1.detect()
    if switch is not None and switch != switch1:
        switch1 = switch

machine.Timer(period=100, mode=machine.Timer.PERIODIC, callback=detect_isr)

# Main loop
while True:
    if switch0 is None:
        print("0: Default (none)")
    else:
        print("0: {}".format(switch0.label))

    if switch1 is None:
        print("1: Default (none)")
    else:
        print("1: {}".format(switch1.label))

    time.sleep_ms(2000)
