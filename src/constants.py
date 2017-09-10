

CONFIG_FILE_PATH = './config.json' # This is gitignored and must be user-created
MOCK_BUILDS_PATH = './mock-builds.json'

NEOPIXEL_LED_COUNT = 8
NEOPIXEL_LED_PIN = 18
NEOPIXEL_LED_FREQ_HZ = 800000
NEOPIXEL_LED_DMA = 5
NEOPIXEL_LED_BRIGHTNESS = 30
NEOPIXEL_LED_INVERT = False

MAX_FADE_BRIGHTNESS = 256
CHECK_BUILDS_INTERVAL = 12 # seconds

RED = {
  'r': 30,
  'g': 0,
  'b': 0
}

GREEN = {
  'r': 0,
  'g': 30,
  'b': 0
}

BLUE = {
  'r': 0,
  'g': 0,
  'b': 30
}

YELLOW = {
  'r': 20,
  'g': 20,
  'b': 0
}

GREY = {
  'r': 0,
  'g': 0,
  'b': 0
}

PINK = {
  'r': 28,
  'g': 6,
  'b': 6
}

DISABLED = {
  'r': 0,
  'g': 0,
  'b': 0
}

# TODO update color map for all possible build colors (and implement fading for build anims?)
# https://github.com/jenkinsci/jenkins/blob/master/core/src/main/java/hudson/model/BallColor.java
STATUSES_MAP = {
  'blue': {
    'hues': BLUE,
    'animated': False
  },
  'blue_anime': {
    'hues': BLUE,
    'animated': True
  },
  'red': {
    'hues': RED,
    'animated': False
  },
  'red_anime': {
    'hues': RED,
    'animated': True
  },
  'yellow': {
    'hues': YELLOW,
    'animated': False
  },
  'yellow_anime': {
    'hues': YELLOW,
    'animated': True
  },
  'green': {
    'hues': GREEN,
    'animated': False
  },
  'green_anime': {
    'hues': GREEN,
    'animated': True
  },
  'grey': {
    'hues': GREY,
    'animated': False
  },
  'grey_anime': {
    'hues': GREY,
    'animated': True
  },
  'aborted': {
    'hues': PINK,
    'animated': False
  },
  'aborted_anime': {
    'hues': PINK,
    'animated': True
  },
  'notbuilt': {
    'hues': GREY,
    'animated': False
  },
  'notbuilt_anime': {
    'hues': GREY,
    'animated': True
  },
  'disabled': {
    'hues': DISABLED,
    'animated': False
  }
}
