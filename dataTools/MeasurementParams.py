
from dataclasses import dataclass
import dataTools.UnitConverter as uc
import Config

@dataclass
class MeasurementParams:
    preamble = bytes("*B", 'utf-8')                                         #     start measurement
    preload: int                                                            #     int16_t preload;
    preloadTime: int                                                        #     uint16_t preloadTime;
    maxLoad: int                                                            #     int16_t maxLoad;
    maxLoadTime: int                                                        #     uint16_t maxLoadTime;
    stepDelay: int                                                          #     uint16_t stepDelay;
    holdDownDelay = int(uc.stepRateToMicros(Config.HOLD_STEP_DOWN_RATE))         #     uint16_t holdDownDelay;
    holdUpDelay = int(uc.stepRateToMicros(Config.HOLD_STEP_UP_RATE))             #     uint16_t holdUpDelay;
    eStopStepDelay = int(uc.stepRateToMicros(Config.EMERGENCY_STOP_STEP_RATE) )  #     uint16_t eStopStepDelay;
    tolerance = int(uc.NewtonToRawADC(Config.TOLERANCE))                         #     uint16_t targetTolerance;
    flipDirection = Config.INVERT_DIR                                       #     bool flip indenter direction