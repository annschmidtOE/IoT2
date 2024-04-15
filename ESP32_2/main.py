import network
import espnow
from machine import Pin, PWM
from utime import sleep, ticks_ms, ticks_diff
from battery_percentage import get_battery_percentage

led = Pin(26, Pin.OUT)
pwm = PWM(led)
pwm.freq(1000)  

def pulse_led(pwm, duration=2, max_duty=1023):
    step_time = 0.01
    steps = int(duration / step_time / 2)

    # Gradually increase brightness
    for duty in range(0, max_duty, max_duty // steps):
        pwm.duty(duty)
        sleep(step_time)

    # Gradually decrease brightness
    for duty in range(max_duty, -1, -(max_duty // steps)):
        pwm.duty(duty)
        sleep(step_time)

    # Return PWM to initial state (LED off)
    pwm.duty(0)
    sleep(30)  # Keep LED off for 30 seconds before next pulse
 

motion = False

def handle_interrupt(pin):
    global motion
    motion = True

pir = Pin(16, Pin.IN)
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

IN1 = Pin(21, Pin.OUT)
IN2 = Pin(22, Pin.OUT)
IN3 = Pin(32, Pin.OUT)
IN4 = Pin(33, Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
sequence1 = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]

station = network.WLAN(network.STA_IF) 
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)
peer = b'\xB0\xA7\x32\xDD\x70\x08'  
esp_now.add_peer(peer)

def open_lit():
    start_time = ticks_ms()  
    while ticks_diff(ticks_ms(), start_time) < 5000:
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def close_lit():
    start_time = ticks_ms()  
    while ticks_diff(ticks_ms(), start_time) < 5000:
        for step in sequence1:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)

def pir_open():
    global motion
    count = 0
    while True:
        pulse_led(pwm, duration=2, max_duty=1023)
        if motion:
            print("ON")
            open_lit()
            close_lit()
            count += 1
            print(f"Antal gange åbnet: {count}")
            battery_percentage = get_battery_percentage()
            string_to_send = f"8c {count} {battery_percentage}"
            esp_now.send(peer, string_to_send)  
            print(string_to_send)
            sleep(5)
            
            print("OFF")
            motion = False  

    return count

        
pir_open()
