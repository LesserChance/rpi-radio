#!/usr/bin/python3

import os
import signal
import subprocess
import sys
import threading

from RPi import GPIO

class RotaryEncoder:

  def __init__(self, gpioA, gpioB, callback=None):

    self.lastGpio = None
    self.gpioA    = gpioA
    self.gpioB    = gpioB
    self.callback = callback

    self.levA = 0
    self.levB = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpioA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.gpioB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(self.gpioA, GPIO.BOTH, self._callback)
    GPIO.add_event_detect(self.gpioB, GPIO.BOTH, self._callback)

  def destroy(self):
    GPIO.remove_event_detect(self.gpioA)
    GPIO.remove_event_detect(self.gpioB)
    GPIO.cleanup()

  def _buttonCallback(self, channel):
    self.buttonCallback(GPIO.input(channel))

  def _callback(self, channel):
    level = GPIO.input(channel)
    if channel == self.gpioA:
      self.levA = level
    else:
      self.levB = level

    # Debounce.
    if channel == self.lastGpio:
      return

    # When both inputs are at 1, we'll fire a callback. If A was the most
    # recent pin set high, it'll be forward, and if B was the most recent pin
    # set high, it'll be reverse.
    self.lastGpio = channel
    if channel == self.gpioA and level == 1:
      if self.levB == 1:
        self.callback(1)
    elif channel == self.gpioB and level == 1:
      if self.levA == 1:
        self.callback(-1)
