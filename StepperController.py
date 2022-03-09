
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM


DEFAULT_STEP_RATE = 1000


class StepperController():

    """Initialize a stepper motor controller. Use pin 12 for step output (hardware PWM) and
    specify the pin for setting motor direction (any GPIO will do)."""
    def __init__(self, directionPinNumber):
        self.directionPin = directionPinNumber

        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(self.directionPin, GPIO.OUT, initial=GPIO.LOW) # initialize direction pin low
        self.pwm = HardwarePWM(pwm_channel=0, hz=DEFAULT_STEP_RATE) # initialize step pin PWM
        self.pwm.start(0) # duty cycle 0 == off
        return


    """Start moving the motor downwards with a step rate of stepFreq"""
    def startMovingDown(self, stepFreq=DEFAULT_STEP_RATE):
        # set the direction pin high to move downwards and start PWM at stepFreq
        GPIO.setup(self.directionPin, GPIO.OUT, initial=GPIO.HIGH)
        self.pwm.change_frequency(stepFreq)
        self.pwm.change_duty_cycle(50)
        return


    """Start moving the motor upwards with a step rate of stepFreq"""
    def startMovingUp(self, stepFreq=DEFAULT_STEP_RATE):
        # set the direction pin low to move upwards and start PWM at stepFreq
        GPIO.setup(self.directionPin, GPIO.OUT, initial=GPIO.LOW)
        self.pwm.change_frequency(stepFreq)
        self.pwm.change_duty_cycle(50)
        return


    """Staop moving the motor"""
    def stopMoving(self):
        self.pwm.change_duty_cycle(0)
        return

