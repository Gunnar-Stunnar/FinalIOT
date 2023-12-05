import sys, time
import RPi.GPIO as GPIO

redPin   = 11
greenPin = 13
bluePin  = 15

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

def main():

    flare = 0
    while True:
        if flare % 2 == 0:
            blink(redPin)
        
        if  flare % 3 == 0:
            blink(greenPin)

        if  flare % 3 == 0:
            blink(bluePin)

        time.sleep(1)
        turnOff(redPin)
        turnOff(greenPin)
        turnOff(bluePin)

if __name__ == "__main__":
     main()