
from dataclasses import dataclass
import dataTools.UnitConverter as uc
import Config

REGULAR_TEST_CODE = bytes("R", 'utf-8')
PPT_TEST_CODE = bytes("T", 'utf-8')
PPI_TEST_CODE = bytes("I", 'utf-8')
TEMPORAL_SUMMATION_TEST_CODE = bytes("S", 'utf-8')

@dataclass
class MeasurementParams:
    preamble = bytes("*B", 'utf-8')                                             #   start measurement
    preload: int                                                                #   int16_t preload;
    preloadTime: int                                                            #   uint16_t preloadTime;
    maxLoad: int                                                                #   int16_t maxLoad;
    maxLoadTime: int                                                            #   uint16_t maxLoadTime;
    stepDelay: int                                                              #   uint16_t stepDelay;
    holdDownDelay = int(uc.stepRateToMicros(Config.HOLD_STEP_DOWN_RATE))        #   uint16_t holdDownDelay;
    holdUpDelay = int(uc.stepRateToMicros(Config.HOLD_STEP_UP_RATE))            #   uint16_t holdUpDelay;
    eStopStepDelay = int(uc.stepRateToMicros(Config.EMERGENCY_STOP_STEP_RATE) ) #   uint16_t eStopStepDelay;
    tolerance = int(uc.NewtonToRawADC(Config.TOLERANCE))                        #   uint16_t targetTolerance;
    iterations = 1                                                              #   how many times to run the test
    flipDirection = Config.INVERT_DIR                                           #   bool flip indenter direction
    testType = REGULAR_TEST_CODE                                                #   which type of test to run
