
from dataclasses import dataclass
import dataTools.UnitConverter as uc
import Config


@dataclass
class MeasurementParams:
    preamble = bytes("*B", 'utf-8')                                             #   start measurement
    preload: int                                                                #   int16_t preload;
    preloadTime: int                                                            #   uint16_t preloadTime;
    maxLoad: int                                                                #   int16_t maxLoad;
    maxLoadTime: int                                                            #   uint16_t maxLoadTime;
    stepDelay: int                                                              #   uint16_t stepDelay;
    testType: bytes                                                             #   which type of test to run
    holdKp = float(Config.HOLD_KP)                                              #   float32 holdKp;
    holdKi = float(Config.HOLD_KI)                                              #   float32 holdKi;
    eStopStepDelay = int(uc.stepRateToMicros(Config.EMERGENCY_STOP_STEP_RATE) ) #   uint16_t eStopStepDelay;
    tolerance = int(uc.NewtonToRawADC(Config.TOLERANCE))                        #   uint16_t targetTolerance;
    iterations = 1                                                              #   how many times to run the test
    flipDirection = Config.INVERT_Z_DIR                                         #   bool flip indenter direction
    constantVacuum = False                                                      #   should the vacuum run constantly in a regular measurement?
