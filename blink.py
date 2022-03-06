from machine import Pin
from time import sleep

led = Pin(15, Pin.OUT)

while True:
    led.toggle()
    sleep(0.1)
