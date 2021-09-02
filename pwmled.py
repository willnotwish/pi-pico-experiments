from machine import Pin, PWM

led = PWM(Pin(25))

def ledon(brightness=65535):
    led.duty_u16(brightness)
