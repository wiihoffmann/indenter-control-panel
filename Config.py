
# This file contains the configuration variables for the indenter.

######## preload settings #########
DEFAULT_PRELOAD_TIME = 1        # seconds
DEFAULT_PRELOAD = 5             # newtons
MIN_PRELOAD = 5                 # newtons
MAX_PRELOAD = 30                # newtons
PRELOAD_INCREMENT_SIZE = 1      # newtons

######## full load settings #######
DEFAULT_MAX_LOAD_TIME = 2       # seconds
DEFAULT_MAX_LOAD = 60           # newtons
MIN_LOAD = 5                    # newtons
MAX_LOAD = 110                  # newtons
MAX_LOAD_INCREMENT_SIZE = 5     # newtons

######## hold time settings #######
MIN_HOLD_TIME = 0               # seconds
MAX_HOLD_TIME = 15              # seconds
HOLD_TIME_INCREMENT_SIZE = 1    # seconds

######## step rate settings #######
EMERGENCY_STOP_STEP_RATE = 1500 # steps/second (How fast to retract indenter during an emergency stop.)
JOG_SPEED = 2000                # steps/second (Manual move up/down speed.)
DEFAULT_STEP_RATE = 1500        # steps/second (Default rate used when taking a measurement.)
MIN_STEP_RATE = 1000            # steps/second
MAX_STEP_RATE = 2500            # steps/second
STEP_RATE_INCREMENT_SIZE = 100  # steps/second

######### misc settings ###########
GRAPH_REFRESH_DELAY = 250       # milliseconds
TOLERANCE = 1                   # newtons (Max deviance from target load when holding.)
SAMPLE_RATE = 1000              # samples/second (Target sampling rate. Actual will vary slightly)

####### hardware calibration ######
""" To calibrate the device, we need to calculate △load / △V (N/V). To do this, apply
two different loads to the indenter and record the corresponding output voltage. The 
calculation assumes that a larger load produces a larger output voltage. """
# first load/voltage calibration pair
CAL_LOAD_1 = 0                  # newtons
CAL_VOLTAGE_1 = 0               # volts
# second load/voltage calibration pair
CAL_LOAD_2 = 100                # newtons
CAL_VOLTAGE_2 = 2.00            # volts

