# Loop test

from machine import Pin
import time

pin = Pin(0, Pin.OUT)

while True:
    pin.toggle()
    # time.sleep_us(1)