from machine import Pin
from utime import sleep

# GPIO pin designations
pin20 = Pin(20)
pin21 = Pin(21)

i2c = machine.I2C(0, sda=pin20, scl=pin21, freq=400000)

from ssd1306 import SSD1306_I2C

oled = SSD1306_I2C(128, 32, i2c)

oled.fill(0)
sleep(1)
oled.show()
oled.text('Hello Caroline', 0, 0)
oled.show()
sleep(2)
oled.text('Hello Mont', 0, 9)
oled.show()
sleep(2)
oled.text('Hello Sash', 0, 18)
oled.show()
sleep(2)

led = Pin(25, Pin.OUT)
while True:
    led.toggle()
    sleep(0.08)
