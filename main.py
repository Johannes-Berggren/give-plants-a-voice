import time
from gpiozero import MCP3008
from gpiozero import LED
import RPi.GPIO as GPIO
import subprocess

# Config
moisture_threshold_lower = 350 # When to ask for water
moisture_threshold_upper = 500 # When to say thank you
escalation_delay = 3600 # One hour (In seconds)

# Pins
moisture_sensor_pin = 5
pir_pin = 21
red_led = LED(16)
green_led = LED(19)
yellow_led = LED(13)
blue_led = LED(12)

moisture_sensor = MCP3008(channel=0, select_pin=moisture_sensor_pin)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)
disgruntlement = 0
last_notification = 0

# led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)

def moisture_below_lower_threshold():
    return moisture_sensor.value * 1023 <= moisture_threshold_lower 

def moisture_above_upper_threshold():
    return moisture_sensor.value * 1023 >= moisture_threshold_upper 

def pir_active():
    return GPIO.input(pir_pin) == 1

def ask_for_water():
    print('Disgruntled!, level: ', disgruntlement)

    if disgruntlement == 1:
        subprocess.call(["mpg123", "audio/Torst 8.mp3"])

    if disgruntlement == 2:
        subprocess.call(["mpg123", "audio/Torst 2.mp3"])

    if disgruntlement == 3:
        subprocess.call(["mpg123", "audio/Torst 3.mp3"])
        
    if disgruntlement == 4:
        subprocess.call(["mpg123", "audio/Torst 4.mp3"])
        
    if disgruntlement == 5:
        subprocess.call(["mpg123", "audio/Torst 5.mp3"])
        
    if disgruntlement == 6:
        subprocess.call(["mpg123", "audio/Torst 6.mp3"])
        
    if disgruntlement == 7:
        subprocess.call(["mpg123", "audio/Torst 7.mp3"])
        
    if disgruntlement >= 8:
        subprocess.call(["mpg123", "audio/Torst 8.mp3"])

def say_thank_you():
    subprocess.call(["mpg123", "audio/Takk 1.mp3"])
    print('Thank you!')
    
def say_thank_you2():
    subprocess.call(["mpg123", "audio/Takk 2.mp3"])
    print('Thank you I love you!')

while (1):
    print('Moisture: ', '{:.0f}'.format(moisture_sensor.value * 1023))
    print(moisture_sensor.value)
    print('PIR: ', GPIO.input(pir_pin))
    print('Disgruntlement: ', disgruntlement)
    print('Last Notification: ', last_notification)
    print('Next Notification: ', escalation_delay - (time.time() - last_notification))
    print('----------')

    if moisture_below_lower_threshold():
        red_led.on() # red
        green_led.off()
        yellow_led.off()
    elif moisture_above_upper_threshold():
        green_led.on() # green
        red_led.off()
        yellow_led.off()
    else:
        yellow_led.on() # yellow
        red_led.off()
        green_led.off()

    if moisture_below_lower_threshold() and pir_active() and time.time() >= last_notification + escalation_delay:
        disgruntlement += 1
        ask_for_water()
        last_notification = time.time()
        
    if disgruntlement > 0 and disgruntlement < 4 and moisture_above_upper_threshold() and pir_active():
        say_thank_you()
        disgruntlement = 0
              
    if disgruntlement >= 4 and moisture_above_upper_threshold() and pir_active():
        say_thank_you2()
        disgruntlement = 0
        
    if pir_active():
        blue_led.on()
    else:
        blue_led.off()

    time.sleep(1)
