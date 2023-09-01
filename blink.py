import time
import rp2
from machine import Pin
import adafruit_dht
# import sys

# print("Python version")
# print(sys.version)
# print("Version info.")
# print(sys.version_info)

board_led = Pin("LED", Pin.OUT, value=1)
small_led = Pin(21, Pin.OUT, value=1)
lone_led = Pin(13, Pin.OUT, value=1)

# dht_pin = Pin(22, Pin.IN, Pin.PULL_UP)
# dht_sensor = adafruit_dht.DHT22(dht_pin)

while True:
    board_led.toggle()
    time.sleep(0.5)
    board_led.toggle()
    time.sleep(0.5)

    small_led.toggle()
    time.sleep(0.5)
    small_led.toggle()
    time.sleep(0.5)

    lone_led.toggle()
    time.sleep(0.5)
    lone_led.toggle()
    time.sleep(0.5)
    # try:
    #     temperature = dht_sensor.temperature
    #     humidity = dht_sensor.humidity
    #     print(f"Temperature: {temperature} °C")
    #     print(f"Humidity: {humidity}%")
    # except RuntimeError as e:
    #     print("Error reading from AM2302: ", str(e))
    #     time.sleep(2.0)