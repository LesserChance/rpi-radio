#!/usr/bin/python
import time
import threading

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class TextScroller (threading.Thread):

    RST = 24
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    PADDING = 2
    SCROLL_SPACE = 0

    text = None
    disp = None
    font = None
    scroll_thread = None

    def __init__(self, text):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.text = text

        self.initDisplay()
        self.initDimensions()
        self.font = ImageFont.truetype('assets/font/upheavtt.ttf', 32)

    def run(self):
        self.scroll(self.text)

    def stop(self):
        self._stop_event.set()
        self.clear()

    def stopped(self):
        return self._stop_event.is_set()

    def initDisplay(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST, dc=self.DC, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=8000000))
        self.disp.begin()
        self.clear()

    def clear(self):
        self.disp.clear()
        self.disp.display()

    def initDimensions(self):
        self.WIDTH = self.disp.width
        self.HEIGHT = self.disp.height
        self.TOP = self.PADDING
        self.BOTTOM = self.HEIGHT - self.PADDING
        self.SCROLL_SPACE = self.WIDTH / 2

    def scroll(self, text):
        image = Image.new('1', (self.WIDTH, self.HEIGHT))
        draw = ImageDraw.Draw(image)

        x = self.PADDING
        text_width = draw.textsize(text, font=self.font)[0]
        min_x = -1 * (text_width + (self.PADDING) + self.SCROLL_SPACE)

        if (text_width > self.WIDTH):
            # scroll the text
            while (not self.stopped()):
                draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), outline=0, fill=0)
                draw.text((x, self.TOP), text, font=self.font, fill=255)

                if (x < text_width):
                    draw.text((x - min_x, self.TOP), text, font=self.font, fill=255)

                x -= 1
                if (x < min_x):
                    x = 0 - self.PADDING

                # Display image
                self.disp.image(image)
                self.disp.display()
                time.sleep(.001)

            self.clear()
        else:
            # do not scroll
            draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), outline=0, fill=0)
            draw.text((x, self.TOP), text, font=self.font, fill=255)
            self.disp.image(image)
            self.disp.display()
