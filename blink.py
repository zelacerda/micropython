from utime import sleep
from machine import Pin

led = machine.Pin(5, Pin.OUT)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)