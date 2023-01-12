import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket
import utime
import uasyncio as asyncio

## Variables
interval = 0.5

## Set Wifi Country
# to avoid possible errors
rp2.country('US')

wlan = network.WLAN(network.STA_IF)

## Return Wifi settings
def ret_wifi_mac():
    # See the MAC address in the wireless chip OTP
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print('mac = ' + mac)

## Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

## Return Wifi Channel
def ret_wifi_chan():
    print('Wifi Channel: ' + str(wlan.config('channel')))

## Return Wifi SSID
def ret_wifi_chan():
    print('Wifi SSID: ' + wlan.config('essid'))

## Return Wifi Power
def ret_wifi_pow():
    print('Wifi Power: ' +str(wlan.config('txpower')))


# Define blinking function for onboard LED to indicate error codes
def blink_onboard_led(num_blinks):
    led_onboard = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led_onboard.on()
        time.sleep(.2)
        led_onboard.off()
        time.sleep(.2)

def blink_led(frequency = 0.5, num_blinks = 3):
    led_onboard = machine.Pin('LED', machine.Pin.OUT)
    for _ in range(num_blinks):
        led_onboard.on()
        time.sleep(frequency)
        led_onboard.off()
        time.sleep(frequency)

## Functions
async def connect_to_wifi():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Diable powersave mode
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('Connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

async def serve_client(reader, writer):

    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

    if sensor_value:
            writer.write(get_html('OPEN'))
        else:
            writer.write(get_html('CLOSED'))

        await writer.drain()
        await writer.wait_closed()

# Function to load in html page
def get_html(index_page = 'index.html'):
    with open(index_page, 'r') as file:
        html = file.read()

    return html

# Setup other LEDS
smallLED = machine.Pin(17, machine.Pin.OUT)

async def main():
    print('Connecting to WiFi...')
    asyncio.create_task(connect_to_wifi())

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

   # print("Service page.")
    while True:
        #sensor_update()

        await asyncio.sleep(interval)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()