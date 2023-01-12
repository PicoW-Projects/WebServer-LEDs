import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket
import utime

# Set country to avoid possible errors
rp2.country('US')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

# Connect to the ssid
wlan.connect(ssid, pw)

# Other things to query
print('Wifi Channel: ' + str(wlan.config('channel')))
print('Wifi SSID: ' + wlan.config('essid'))
print('Wifi Power: ' +str(wlan.config('txpower')))

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

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

# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    blink_led(0.2, 5)
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    blink_led(1, 2)

# Function to load in html page
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()

    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)
led_onboard = machine.Pin('LED', machine.Pin.OUT)

# Setup other LEDS
smallLED = machine.Pin(17, machine.Pin.OUT)

# Listen for connections
while True:
    try:

        smallLED.on()
        utime.sleep(2)
        smallLED.off()
        utime.sleep(1)

        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # Print or hide response
        # print(r)

        r = str(r)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')
        print('led_on = ', led_on)
        print('led_off = ', led_off)
        if led_on > -1:
            print('LED ON')
            led_onboard.value(1)

        if led_off > -1:
            print('LED OFF')
            led_onboard.value(0)

        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')