import paho.mqtt.publish as publish
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import serial as ser
from threading import Thread
from queue import Queue

TRIG = 17
ECHO = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

data = ser.Serial("/dev/ttyS0", 9600, timeout=2)
received_data_queue = Queue()

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start_time = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def send_distance():
    while True:
        distance = measure_distance()
        neopixel = 3

        if distance < 5:
            neopixel = 1
        elif distance > 5 and < 10:
            neopixel = 2
        else:
            neopixel = 3

        message = str(neopixel).encode('ascii')

        received_data = data.read(data.in_waiting).decode('ascii')

        received_data_queue.put(received_data)

        data.write(message)
        time.sleep(5)

def publish_distance():
    while True:
        distance = measure_distance()
        payload = f"distance: {distance}"
        publish.single("8c/sensor", str(payload), hostname="13.74.244.39")
        time.sleep(1)
        print("Distance: ", distance)

receive_thread = Thread(target=send_distance)
publish_thread = Thread(target=publish_distance)

receive_thread.start()
publish_thread.start()

try:
    while True:
        if not received_data_queue.empty():
            
            received_data = received_data_queue.get()
            print(f"gange åbnet samt batteri: {received_data}")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgrammet blev stoppet.")
    GPIO.cleanup()
    data.close()