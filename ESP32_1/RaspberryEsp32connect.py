import sys, uselect
from machine import UART, Pin
from neopixel import NeoPixel
from time import sleep
import network
import espnow

station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

uart_port = 2
uart_speed = 9600

uart = UART(uart_port, uart_speed)  # Initialize UART

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)  # Register stdin for polling

print("ESP32 USB <-> UART <-> UART <-> ESP USB program")

n = 12  # Number of NeoPixels
p = 26  # Pin number
np = NeoPixel(Pin(p, Pin.OUT), n)  # Initialize NeoPixel

def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()

def clear():
    set_color(0, 0, 0)
    
def red():
    set_color(255, 0, 0)
    
def yellow():
    set_color(255, 255, 0)

def green():
    set_color(0, 255, 0)

while True:
    # Check for ESP-NOW message
    host, msg = esp_now.recv()
    if msg is not None and "8c" in msg:  # Ensure msg is not None before checking its content
       print("ESP-NOW Received:", msg)
       uart.write(msg)  
    
    # Check for UART message
    if uart.any() > 0:
        raw_string = uart.read()
        if raw_string:  # Ensure raw_string is not None
            string = raw_string.decode('utf-8', 'ignore').strip()  # Decode with 'ignore' for errors and strip()
            print("UART Received:", string)
            # Handle different cases based on the received string
            if string == "1":
                green()
                sleep(0.5)
                clear()
            elif string == "2":
                yellow()
                sleep(0.5)
                clear()
            elif string == "3":
                red()
                sleep(0.5)
                clear()
    
    # Poll for input from USB
    poll_result = usb.poll(0)
    if poll_result:  # If there's something to read
        ch = sys.stdin.read(1)
        uart.write(ch.encode('utf-8')) 

