import network
import espnow
from machine import Pin, PWM
from utime import sleep
from time import sleep, localtime, time
from utime import sleep_ms, ticks_ms, ticks_diff
from battery_percentage import get_battery_percentage

led = Pin(26, Pin.OUT)


pwm = PWM(led)

#
pwm.freq(1000) #FUCK GITHUB

def pulse_led(pwm, duration=2, max_duty=1023):
    step_time = 0.01  # Time between duty cycle steps (10ms)
    steps = int(duration / step_time / 2)  # Calculate the number of steps for fading in/out

    # Gradually increase brightness
    for duty in range(0, max_duty, max_duty // steps):
        pwm.duty(duty)
        sleep(step_time)

    # Gradually decrease brightness
    for duty in range(max_duty, -1, -(max_duty // steps)):
        pwm.duty(duty)
        sleep(step_time)

    # Introduce a brief off period before the next pulse starts, adjust this to decrease the off time
    sleep(10)  # Off time between pulses, decrease this value to reduce off time

IR_Sensor = Pin(16, Pin.IN, Pin.PULL_DOWN)
SPEAKER_PIN = 17

speaker = PWM(Pin(SPEAKER_PIN))

pb1 = Pin(4, Pin.IN)
pb2 = Pin(0, Pin.IN)

IN1 = Pin(21,Pin.OUT)
IN2 = Pin(22,Pin.OUT)
IN3 = Pin(32,Pin.OUT)
IN4 = Pin(33,Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
sequence1 = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]

# A WLAN interface must be active to send()/recv()
station = network.WLAN(network.STA_IF) # Or network.AP_IF
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)
peer = b'\xB0\xA7\x32\xDD\x70\x08'  # MAC address of peer's wifi interface
esp_now.add_peer(peer)   # Must add_peer() before send()

def sound_off():
   speaker.duty_u16(0)

def IRsen_tone():
   speaker.duty_u16(1000)
   speaker.freq(300)
   sleep(.5) 
   sound_off()

def forward_tone():
   speaker.duty_u16(1000)
   speaker.freq(400)
   sleep(.1)
   speaker.freq(900)
   sleep(.1)
   speaker.freq(1200)
   sleep(.1)
   sound_off()

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

def ir_open():
    count = 0
    driver_state = 0
    battery_percentage = get_battery_percentage()
    while True:
        if IR_Sensor.value() == 0:
            print("ON")
            IRsen_tone()
            driver_state = 2
            open_lit()
            close_lit()
            count += 1
            print(f"Antal gange åbnet: {count}")
            string_to_send = f"8c {count} {battery_percentage}"
            
            esp_now.send(peer, string_to_send) 
            print(string_to_send)
            
        if IR_Sensor.value():
            print("Forward!")
            driver_state = 1
        pulse_led(pwm, duration=10) 
        sleep(1)
    return count
        
ir_open()