import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import threading

pulseDelay = .00001
moving = False


def moveAsync(direction):
    if direction == 1:
        GPIO.setup(10, GPIO.OUT, initial=GPIO.HIGH)
    else:
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)

    while moving == True:
        GPIO.output(8, GPIO.HIGH) # Turn on
        time.sleep(pulseDelay) # Sleep for 1 second
        GPIO.output(8, GPIO.LOW) # Turn off
        time.sleep(pulseDelay) # Sleep for 1 second


class Controller():
    
    def __init__(self, stepPin, directionPin):
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(stepPin, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(directionPin, GPIO.OUT, initial=GPIO.LOW)
        self.stepPin = stepPin
        self.directionPin = directionPin


    def startMovingDown(self):
        global moving
        moving = True
        # direction 1 for down
        threading.Thread(target=moveAsync, args=(1,)).start()


    def stopMovingDown(self):
        global moving
        moving = False


    def startMovingUp(self):
        global moving
        moving = True
        # direction 0 for up
        threading.Thread(target=moveAsync, args=(0,)).start()


    def stopMovingUp(self):
        global moving
        moving = False