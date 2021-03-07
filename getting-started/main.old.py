from machine import Pin
import time

pin = Pin(25, Pin.OUT)
print("About to flash...")
while True:
  pin.toggle()
  print(".")
  time.sleep_ms(1000)
