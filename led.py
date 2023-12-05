import sys, time
import RPi.GPIO as GPIO

redPin   = 11
greenPin = 13
bluePin  = 15




def main():

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(redPin, GPIO.OUT)
    GPIO.setup(greenPin, GPIO.OUT)
    GPIO.setup(bluePin, GPIO.OUT)

    Freq = 100
    RED = GPIO.PWM(redPin, Freq)
    GREEN = GPIO.PWM(greenPin, Freq)
    BLUE = GPIO.PWM(bluePin, Freq)

    RED.start(100)
    GREEN.start(1)
    BLUE.start(1)

    while True:
        for x in range(1,101):
            GREEN.ChangeDutyCycle(x)
            time.sleep(0.05)
        
        for x in range(1,101):
            RED.ChangeDutyCycle(x)
            time.sleep(0.05)
        
        for x in range(1,101):
            BLUE.ChangeDutyCycle(x)
            time.sleep(0.05)
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()