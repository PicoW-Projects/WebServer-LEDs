import time
from machine import Pin

board_led = Pin("LED", Pin.OUT, value=1)
small_led = Pin(21, Pin.OUT, value=1)
red_led = Pin(9, Pin.OUT, value=1)
green_led = Pin(10, Pin.OUT, value=1)

while True:
    board_led.toggle()
    time.sleep(0.5)
    board_led.toggle()
    time.sleep(0.5)

    small_led.toggle()
    time.sleep(0.5)
    small_led.toggle()
    time.sleep(0.5)

    red_led.toggle()
    time.sleep(0.5)
    red_led.toggle()
    time.sleep(0.5)

    green_led.toggle()
    time.sleep(0.5)
    green_led.toggle()
    time.sleep(0.5)