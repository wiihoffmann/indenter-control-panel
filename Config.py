
# This file contains the configuration variables for the indenter and its tests.

######## preload settings #########
STIFFNESS_DEFAULT_PRELOAD = 8       # newtons (for regular stiffness test)
MIN_PRELOAD = 5                     # newtons
MAX_PRELOAD = 30                    # newtons
PRELOAD_INCREMENT_SIZE = 1          # newtons

######## full load settings #######
STIFFNESS_DEFAULT_MAX_LOAD = 100    # newtons (for regular stiffness test)
PPT_DEFAULT_MAX_LOAD = 100          # newtons (for PPT test)
PPI_DEFAULT_MAX_LOAD = 40           # newtons (for PPI test)
TEMP_SUMM_DEFAULT_MAX_LOAD = 40     # newtons (for temporal summation test)
MIN_LOAD = 5                        # newtons
MAX_LOAD = 110                      # newtons
MAX_LOAD_INCREMENT_SIZE = 5         # newtons

######## hold time settings #######
STIFFNESS_DEFAULT_PRELOAD_TIME = 1      # seconds (preload time for regular stiffness test)
STIFFNESS_DEFAULT_MAX_LOAD_TIME = 2     # seconds (full load time for regular stiffness test)
PPI_DEFAULT_LOAD_TIME = 3               # seconds (full load time for regular stiffness test)
MIN_HOLD_TIME = 0                       # seconds
MAX_HOLD_TIME = 15                      # seconds
HOLD_TIME_INCREMENT_SIZE = 1            # seconds

#### measurement speed settings ###
STIFFNESS_DEFAULT_STEP_RATE = 600       # steps/second (Default rate used when taking a regular stiffness measurement.)
PPT_DEFAULT_STEP_RATE = 600             # steps/second (Default rate used when doing a PPT test.)
PPI_DEFAULT_STEP_RATE = 600             # steps/second (Default rate used when doing a PPI test.)
TEMP_SUMM_DEFAULT_STEP_RATE = 600       # steps/second (Default rate used when doing a temporal summation test.)
MIN_STEP_RATE = 200                     # steps/second
MAX_STEP_RATE = 1500                    # steps/second
STEP_RATE_INCREMENT_SIZE = 100          # steps/second

#### repeat measurement settings ###
STIFFNESS_DEFAULT_REPEAT_COUNT = 1      # default number of times to repeat a measurement (for regular stiffness test)
PPT_DEFAULT_REPEAT_COUNT = 1            # default number of times to repeat a measurement (for PPT test)
PPI_DEFAULT_REPEAT_COUNT = 1            # default number of times to repeat a measurement (for PPI test)
TEMP_SUMM_DEFAULT_REPEAT_COUNT = 10     # default number of times to repeat a measurement (for temporal summation test)
MIN_REPEAT_COUNT = 1                    # steps/second
MAX_REPEAT_COUNT = 15                   # steps/second
REPEAT_COUNT_INCREMENT_SIZE = 1         # steps/second

### misc. measurement settings ####
TOLERANCE = 2.5                 # newtons (Max deviance from target load when holding.)
HOLD_STEP_UP_RATE = 100         # steps/second (when holding, how fast can we move up to maintain the target load)
HOLD_STEP_DOWN_RATE = 100       # steps/second (when holding, how fast can we move down to maintain the target load)

##### graph display settings #####
GRAPH_COLORS = 10               # how many colors we can use on the graph comparison screen
GRAPH_LINE_WIDTH = 3            # width of the graph line
GRAPH_REFRESH_DELAY = 250       # milliseconds
GRAPH_MAX_POINTS = 8000         # The max number of data points to show on the live graph at once.

######### misc. settings ##########
EMERGENCY_STOP_STEP_RATE = 2000    # steps/second (How fast to retract indenter during an emergency stop.)
JOG_SPEED_X = 1600                 # steps/second (Manual move up/down speed.)
JOG_SPEED_Y = 1600                 # steps/second (Manual move left/right speed.)
JOG_SPEED_Z = 1200                 # steps/second (Manual move forward/backward speed.)
INVERT_X_DIR = True                # Set to True if the indenter moves closer when it should move farther away
INVERT_Y_DIR = True                # Set to True if the indenter moves left when it should move right
INVERT_Z_DIR = True                # Set to True if the indenter moves up when it should move down
FULLSCREEN_MODE = True             # Should the program open in fullscreen?
SHOW_KEYBOARD = True               # show the keyboard when saving?

####### hardware calibration ######
""" To calibrate the device, we need to calculate △load / △V (N/V). To do this, apply
two different loads to the indenter and record the corresponding output voltage. The 
calculation assumes that a larger load produces a larger output voltage. """
# first load/voltage calibration pair
CAL_READING_1 = 24.77025    # newtons
CAL_VOLTAGE_1 = 7756.32643  # raw ADC value
# second load/voltage calibration pair
CAL_READING_2 = 103.58379   # newtons
CAL_VOLTAGE_2 = 15418.93992 # raw ADC value

