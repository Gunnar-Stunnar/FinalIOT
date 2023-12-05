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

    sin_x, x = 1, 0
    sin_y, y = 1, 0
    sin_z, z = 1, 0

    while True:

        
        GREEN.ChangeDutyCycle(x)
        RED.ChangeDutyCycle(y)
        BLUE.ChangeDutyCycle(z)

        x += sin_x * 0.1
        y += sin_y * 0.3
        z += sin_z * 0.001

        if x > 100:
            sin_x = -1
        elif x < 0:
            sin_x = 1
        
        if y > 100:
            sin_y = -1
        elif y < 0:
            sin_y = 1

        if z > 100:
            sin_z = -1
        elif z < 0:
            sin_z = 1

        time.sleep(0.01)      

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()