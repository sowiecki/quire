import threading
import time
import sys
import json
import requests
from functools import partial

import microdotphat
from luma.core.serial import i2c, spi
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.oled.device import ssd1306

from neopixel import Adafruit_NeoPixel

import constants
import utils

OLED_SERIAL = i2c(port = 1, address=0x3C)
OLED_SCREEN = ssd1306(OLED_SERIAL, rotate = 1)
VIRTUAL_OLED_SCREEN = viewport(OLED_SCREEN, width = OLED_SCREEN.width, height = 768)

NEOPIXEL_STRIP = Adafruit_NeoPixel(
  constants.NEOPIXEL_LED_COUNT,
  constants.NEOPIXEL_LED_PIN,
  constants.NEOPIXEL_LED_FREQ_HZ,
  constants.NEOPIXEL_LED_DMA,
  constants.NEOPIXEL_LED_INVERT,
  constants.NEOPIXEL_LED_BRIGHTNESS
)

builds = {}

def setup(CONFIG):
  getBuilds(CONFIG)
  microdotphat.clear()
  microdotphat.write_string(CONFIG['phatText'], kerning = False)

def phat():
  while True:
    microdotphat.scroll()
    microdotphat.show()
    time.sleep(0.01)

def oled():
  while True:
    font = None

    with canvas(VIRTUAL_OLED_SCREEN) as draw:
      for index, job in enumerate(builds['jobs']):
        branchName = job['name']
        buildStatusIndicator = utils.genBuildStatusIndicator(index, job)
        draw.text((-1, index * 16), buildStatusIndicator, font = font, fill = "white")
        draw.text((16, index * 16), branchName, font = font, fill = "white")
    time.sleep(0.05)

def neopixel():
  def lightPixels(i):
    if i <= constants.MAX_FADE_BRIGHTNESS / 2:
      fadeModifier = i
    elif i > constants.MAX_FADE_BRIGHTNESS / 2:
      fadeModifier = constants.MAX_FADE_BRIGHTNESS - i

    for index, job in enumerate(builds['jobs']):
      pixelToLight = constants.NEOPIXEL_LED_COUNT - 1 - index
      buildStatus = constants.STATUSES_MAP[builds['jobs'][index]['color']]
      if buildStatus['animated']:
        pixelColor = utils.genPixelColor(buildStatus, fadeModifier)
        NEOPIXEL_STRIP.setPixelColor(pixelToLight, pixelColor)
      else:
        pixelColor = utils.genPixelColor(buildStatus)
        NEOPIXEL_STRIP.setPixelColor(pixelToLight, pixelColor)
    NEOPIXEL_STRIP.show()

  while True:
    for i in range(constants.MAX_FADE_BRIGHTNESS):
      lightPixels(i)
      time.sleep(0.002)

def getBuilds(config):
  global builds

  endpoint = config['endpoint']
  username = config['username']
  password = config['password']

  auth = requests.auth.HTTPBasicAuth(username, password)
  builds = requests.get(endpoint, auth=auth).json()

  if '--mocks' in sys.argv:
    with open(constants.MOCK_BUILDS_PATH) as json_data:
      MOCK_BUILDS = json.load(json_data)
    builds['jobs'] = builds['jobs'] + MOCK_BUILDS

  builds['jobs'] = utils.sortJobs(builds['jobs'])

def monitorBuilds(config):
  _getBuilds = partial(getBuilds, config)
  interval = utils.setInterval(_getBuilds, constants.CHECK_BUILDS_INTERVAL)

def run():
  NEOPIXEL_STRIP.begin()

  tasks = [neopixel, phat, oled]

  for task in tasks:
    thread = threading.Thread(target = task)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
  try:
    with open(constants.CONFIG_FILE_PATH) as json_data:
      CONFIG = json.load(json_data)

    setup(CONFIG)
    thread = threading.Thread(target = monitorBuilds, args = (CONFIG,))
    thread.start()

    run()

  except KeyboardInterrupt:
    NEOPIXEL_STRIP._cleanup()
    sys.exit()
    pass
