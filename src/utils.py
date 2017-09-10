import threading
import time
from string import Template

from neopixel import Color

import constants

def setInterval(func, sec):
  def funcWrapper():
    setInterval(func, sec)
    func()
  t = threading.Timer(sec, funcWrapper)
  t.start()
  return t

def genPixelColor(buildStatus, fadeModifier = 0):
  redValue = buildStatus['hues']['r']
  greenValue = buildStatus['hues']['g']
  blueValue = buildStatus['hues']['b']
  r = redValue + fadeModifier / 4 if redValue == 0 else redValue + fadeModifier
  g = greenValue + fadeModifier / 4 if greenValue == 0 else  greenValue + fadeModifier
  b = blueValue + fadeModifier  / 4 if blueValue == 0 else  blueValue + fadeModifier
  return Color(g, r, b)

def genBuildStatusIndicator(index, job):
  buildStatus = constants.STATUSES_MAP[job['color']]
  if buildStatus['animated']:
    return Template('[${i}]').substitute({ 'i': index + 1 })
  else:
    return Template(' ${i} ').substitute({ 'i': index + 1 })

def sortJobs(jobs):
  def filterJob(job):
    jobs.remove(job)
    return job

  def timestamp(job):
    try:
      return job['lastBuild']['timestamp']
    except KeyError:
      return 0

  master = [filterJob(job) for job in jobs if job['name'] == 'master'][0]
  develop = [filterJob(job) for job in jobs if job['name'] == 'develop'][0]
  sortedJobs = sorted(jobs, key=timestamp, reverse=True)
  newestJobs = sortedJobs[:constants.NEOPIXEL_LED_COUNT - 2]

  return [master, develop] + newestJobs
