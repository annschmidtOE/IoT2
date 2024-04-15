import sys, uselect
from machine import UART, Pin
from neopixel import NeoPixel
from time import sleep
import network
import espnow
from battery_percentage import get_battery_percentage

station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

uart_port = 2
uart_speed = 9600

uart = UART(uart_port, uart_speed)  

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)  

print("ESP32 USB <-> UART <-> UART <-> ESP USB program")

n = 12  
p = 26  
np = NeoPixel(Pin(p, Pin.OUT), n)  

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
    battery = get_battery_percentage()
    host, msg = esp_now.recv()
    if msg is not None and "8c" in msg:  
       print("ESP-NOW Received:", msg)
       uart.write(f"{msg} og {battery}")  
    
    if uart.any() > 0:
        raw_string = uart.read()
        if raw_string:  
            string = raw_string.decode('utf-8', 'ignore').strip()  
            print("UART Received:", string)
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
    
    poll_result = usb.poll(0)
    if poll_result:  
        ch = sys.stdin.read(1)
        uart.write(ch.encode('utf-8')) 