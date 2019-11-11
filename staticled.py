#!/usr/bin/python3
import time
import threading
import random

import RPi.GPIO as GPIO

class StaticLed (threading.Thread):

    PIN = 22

    def __init__(self, static_percent):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.static_percent = static_percent

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, GPIO.LOW)

    def run(self):
        self.flicker(self.static_percent)

    def stop(self):
        self._stop_event.set()
        GPIO.output(self.PIN, GPIO.LOW)

    def stopped(self):
        return self._stop_event.is_set()

    def flicker(self, static_percent):
        if (static_percent > 0):
            while (not self.stopped()):
                # turn the led off more freqently if the percent is higher
                chance = random.uniform(0, 1)
                if (chance > (self.static_percent - .1)):
                    GPIO.output(self.PIN, GPIO.HIGH)
                else:
                    GPIO.output(self.PIN, GPIO.LOW)


                time.sleep(random.uniform(.001, .01))
        else:
            # just turn the led on
            GPIO.output(self.PIN, GPIO.HIGH)
