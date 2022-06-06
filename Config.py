
# This file contains the configuration variables for the indenter.

######## preload settings #########
DEFAULT_PRELOAD_TIME = 1        # seconds
DEFAULT_PRELOAD = 8             # newtons
MIN_PRELOAD = 5                 # newtons
MAX_PRELOAD = 30                # newtons
PRELOAD_INCREMENT_SIZE = 1      # newtons

######## full load settings #######
DEFAULT_MAX_LOAD_TIME = 2       # seconds
DEFAULT_MAX_LOAD = 100          # newtons
MIN_LOAD = 5                    # newtons
MAX_LOAD = 110                  # newtons
MAX_LOAD_INCREMENT_SIZE = 5     # newtons

######## hold time settings #######
MIN_HOLD_TIME = 0               # seconds
MAX_HOLD_TIME = 15              # seconds
HOLD_TIME_INCREMENT_SIZE = 1    # seconds

######## step rate settings #######
EMERGENCY_STOP_STEP_RATE = 2000 # steps/second (How fast to retract indenter during an emergency stop.)
JOG_SPEED = 600                 # steps/second (Manual move up/down speed.)
DEFAULT_STEP_RATE = 600         # steps/second (Default rate used when taking a measurement.)
MIN_STEP_RATE = 200             # steps/second
MAX_STEP_RATE = 1500            # steps/second
STEP_RATE_INCREMENT_SIZE = 100  # steps/second

######### misc settings ###########
GRAPH_REFRESH_DELAY = 250       # milliseconds
TOLERANCE = 2.5                 # newtons (Max deviance from target load when holding.)
HOLD_STEP_UP_RATE = 200         # steps/second (when holding, how fast can we move up to maintain the target load)
HOLD_STEP_DOWN_RATE = 200       # steps/second (when holding, how fast can we move down to maintain the target load)
SAMPLE_RATE = 1000              # samples/second (Target sampling rate. Actual will vary slightly)
SHOW_KEYBOARD = True            # show the keyboard when saving?
INVERT_DIR = False              # Set to True if the indenter moves up when it should move down

####### hardware calibration ######
""" To calibrate the device, we need to calculate △load / △V (N/V). To do this, apply
two different loads to the indenter and record the corresponding output voltage. The 
calculation assumes that a larger load produces a larger output voltage. """
# first load/voltage calibration pair
CAL_LOAD_1 = 13.07673                # newtons
CAL_VOLTAGE_1 = 0.511807446121897    # volts
# second load/voltage calibration pair
CAL_LOAD_2 = 103.48569               # newtons
CAL_VOLTAGE_2 = 2.42733884862367     # volts

