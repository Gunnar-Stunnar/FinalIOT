import RPi.GPIO as GPIO
import time
import signal
import sys
import os

# Configuration
FAN_PIN = 1            # BCM pin used to drive PWM fan
WAIT_TIME = 1           # [s] Time to wait between each refresh
PWM_FREQ = 25           # [kHz] 25kHz for Noctua PWM control

FAN_HIGH = 100
FAN_OFF = 0

def setFanSpeed(speed):
    fan.start(speed)
    return()

try:
    # Setup GPIO pin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    setFanSpeed(FAN_OFF)
    # Handle fan speed every WAIT_TIME sec
    while True:
        out = input("Turn on: ")
        if out == "0":
           setFanSpeed(FAN_OFF)
        elif out == "1":
            setFanSpeed(FAN_HIGH)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    print("KILLED")
    setFanSpeed(FAN_HIGH)