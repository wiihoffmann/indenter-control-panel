
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM
import time
import Config


class StepperController():
    """ A class for driving the stepper motor.
    This class allows for driving the stepper motor. It allows for moving the indenter head up
    and down, as well as measuring how far the indenter head has moved in steps.
    """

    def __init__(self, directionPinNumber):
        """ Initialize a stepper motor controller. Use pin 12 for step output (hardware PWM).
        Parameters:
            directionPinNumber (int): GPIO pin for setting motor direction (any GPIO will do)."""

        self.directionPin = directionPinNumber
        self.stepRate = 0
        self.direction = 0
        self.startTime = time.time_ns()

        if(Config.INVERT_DIR):
            self.downPolarity = GPIO.LOW
            self.upPolarity = GPIO.HIGH
        else:
            self.downPolarity = GPIO.HIGH
            self.upPolarity = GPIO.LOW

        GPIO.setwarnings(False)  # Ignore GPIO warnings
        GPIO.setmode(GPIO.BCM)  # Use GPIO pin numbering (as opposed to header pin number)
        GPIO.setup(self.directionPin, GPIO.OUT, initial=self.upPolarity) # initialize direction pin low
        self.pwm = HardwarePWM(pwm_channel=0, hz=100) # initialize step pin PWM
        self.pwm.start(0) # duty cycle 0 == off
        return


    def startMovingDown(self, stepFreq):
        """ Start moving the motor downwards.
        Parameters:
            stepFreq (int): the step rate to move at (steps/second)"""

        self.stepRate = stepFreq
        self.direction = 1  # downwards

        # set the direction pin high to move downwards and start PWM at stepFreq
        GPIO.output(self.directionPin, self.downPolarity)
        self.startTime = time.time_ns()
        self.pwm.change_frequency(stepFreq)
        self.pwm.change_duty_cycle(50)
        return


    def startMovingUp(self, stepFreq):
        """ Start moving the motor upwards.
        Parameters:
            stepFreq (int): the step rate to move at (steps/second)"""

        self.stepRate = stepFreq
        self.direction = -1 # upwards

        # set the direction pin low to move upwards and start PWM at stepFreq
        GPIO.output(self.directionPin, self.upPolarity)
        self.startTime = time.time_ns()
        self.pwm.change_frequency(stepFreq)
        self.pwm.change_duty_cycle(50)
        return


    def stopMoving(self):
        """ Stop moving the stepper motor.
        Returns:
            displacement (int): the displacement of the stepper since the last call
                                to getDisplacement() """

        self.pwm.change_duty_cycle(0)
        displacement = self.getDisplacement()
        self.direction = 0 # not moving
        return displacement


    def getDisplacement(self):
        """ Gets the displacement of the stepper since it started moving, or since the 
            last call to this method; whichever is most recent.
        Returns:
            displacement (int): The displacement of the stepper motor. Positive for downwards,
                                negative for upwards. """

        now = time.time_ns()
        travelTime = (now - self.startTime)* pow(10,-9) # convert from ns to s
        self.startTime = now
        return self.stepRate * travelTime * self.direction

    
    def getDirection(self):
        """ Gets the direction in which the stepper is moving.
        Returns:
            direction (int): The direction of the stepper motor. Positive for downwards,
                             negative for upwards, zero for not moving. """

        return self.direction


    def emergencyStop(self, displacement, stepFreq):
        """ The emergency stop procedure for the stepper motor. Moves the motor back up
            to zero displacement. """

        self.startMovingUp(stepFreq)
        # move up until zero displacement is achieved
        while displacement > 0:
            time.sleep(.001)
            displacement += self.getDisplacement()
        self.stopMoving()

