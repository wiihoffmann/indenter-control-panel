
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
EMERGENCY_STOP_STEP_RATE = 500  # steps/second (How fast to retract indenter during an emergency stop.)
JOG_SPEED = 600                 # steps/second (Manual move up/down speed.)
DEFAULT_STEP_RATE = 600         # steps/second (Default rate used when taking a measurement.)
MIN_STEP_RATE = 200             # steps/second
MAX_STEP_RATE = 1500            # steps/second
STEP_RATE_INCREMENT_SIZE = 100  # steps/second

######### misc settings ###########
GRAPH_REFRESH_DELAY = 250       # milliseconds
TOLERANCE = 2.5                 # newtons (Max deviance from target load when holding.)
HOLD_STEP_UP_RATE = 100         # steps/second (when holding, how fast can we move up to maintain the target load)
HOLD_STEP_DOWN_RATE = 100       # steps/second (when holding, how fast can we move down to maintain the target load)
GRAPH_COLORS = 10               # how many colors we can use on the graph comparison screen
GRAPH_LINE_WIDTH = 3            # width of the graph line
SHOW_KEYBOARD = True            # show the keyboard when saving?
INVERT_DIR = False               # Set to True if the indenter moves up when it should move down

####### hardware calibration ######
""" To calibrate the device, we need to calculate △load / △V (N/V). To do this, apply
two different loads to the indenter and record the corresponding output voltage. The 
calculation assumes that a larger load produces a larger output voltage. """
# first load/voltage calibration pair
CAL_READING_1 = 35.18847    # newtons
CAL_VOLTAGE_1 = 10140       # raw ADC value
# second load/voltage calibration pair
CAL_READING_2 = 92.214      # newtons
CAL_VOLTAGE_2 = 17500       # raw ADC value

