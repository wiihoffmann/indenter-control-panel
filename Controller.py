import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import threading
import time


DEFAULT_STEP_RATE = .001
stepRate = DEFAULT_STEP_RATE
moving = False


def moveAsync(direction):
    pulseDelay = 1/(2*stepRate)

    if direction == 1:
        GPIO.setup(10, GPIO.OUT, initial=GPIO.HIGH)
    else:
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)

    while moving == True:
        GPIO.output(8, GPIO.HIGH) # Turn on
        time.sleep(pulseDelay)
        GPIO.output(8, GPIO.LOW) # Turn off
        time.sleep(pulseDelay)


class Controller():
    
    def __init__(self, stepPin, directionPin):
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(stepPin, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(directionPin, GPIO.OUT, initial=GPIO.LOW)
        self.stepPin = stepPin
        self.directionPin = directionPin


    def startMovingDown(self, stepFreq = DEFAULT_STEP_RATE):
        global moving, stepRate
        moving = True
        stepRate = stepFreq
        # direction 1 for down
        threading.Thread(target=moveAsync, args=(1,)).start()


    def stopMovingDown(self):
        global moving
        moving = False


    def startMovingUp(self, stepFreq = DEFAULT_STEP_RATE):
        global moving, stepRate
        moving = True
        stepRate = stepFreq
        # direction 0 for up
        threading.Thread(target=moveAsync, args=(0,)).start()


    def stopMovingUp(self):
        global moving
        moving = False