#!/usr/bin/python
import RPi.GPIO as GPIO
import sys, select, traceback, math
import mpcplaylistplayer, staticplayer, playlist, textscroller, staticled, rotary
from threading import Event

GPIO.setmode(GPIO.BCM)

PLAYLIST_NAME = 'radio'
MAX_STATIC = 5
MAX_DIAL = 100

DIAL_GPIO_A = 17
DIAL_GPIO_B = 18

SWITCH_GPIO_OUT = 12
SWITCH_GPIO_IN = 25

GPIO.setwarnings(False)
GPIO.setup(SWITCH_GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH_GPIO_OUT, GPIO.OUT)
GPIO.output(SWITCH_GPIO_OUT, GPIO.HIGH)

class Radio:
    played = False
    playing = False

    playlist = None
    text_scroller = None

    channel = None
    radio_player = None

    static = None
    static_led = None
    static_player = None

    dial_num = 0
    dial_channels = [];
    dial_static = [];

    def __init__(self):
        self.playlist = playlist.Playlist(PLAYLIST_NAME)
        self.radio_player = mpcplaylistplayer.MpcPlaylistPlayer()
        self.static_player = staticplayer.StaticPlayer()

        self.dial = rotary.RotaryEncoder(DIAL_GPIO_A, DIAL_GPIO_B, callback=self.handleDial)
        self.generateDialArrays()

    def setPlaying(self, new_playing):
        if (not self.playing and new_playing):
            if (not self.played):
                self.start()
                self.played = True
            else:
                self.runStaticLed()
                self.printChannelName()
                self.radio_player.on()
                self.static_player.on()


        elif (self.playing and not new_playing):
            self.radio_player.off()
            self.static_player.off()

            if (self.text_scroller != None):
                self.text_scroller.stop()
            if (self.static_led != None):
                self.static_led.stop()

        self.playing = new_playing;

    def generateDialArrays(self):
        spacing = int(MAX_DIAL / self.playlist.getChannelCount())
        half_spacing = math.ceil(float(spacing) / 2)
        insert_channel = 0
        insert_static = 0
        static_direction = -1

        for i in range(0,255):
            if ((i - half_spacing) % spacing == 0):
                insert_channel += 1

            if (i % spacing == 0):
                insert_static = 0

            if (insert_static >= half_spacing or insert_static == 0):
                static_direction *= -1

            self.dial_channels.append(insert_channel)
            self.dial_static.append(MAX_STATIC if insert_static > MAX_STATIC else insert_static)

            insert_static += static_direction

    def start(self):
        self.radio_player.start(self.playlist)
        self.setDial(0)

    def printChannelName(self):
        station = self.playlist.getChannelName(self.channel)
        print station

        if (self.text_scroller != None):
            self.text_scroller.stop()

        self.text_scroller = textscroller.TextScroller(station)
        self.text_scroller.start()

    def updateChannel(self, channel):
        prev_channel = self.channel
        self.channel = channel

        if (prev_channel != self.channel):
            self.printChannelName()

        self.radio_player.playChannel(self.channel)

    def updateStatic(self, static):
        prev_static = self.static
        self.static = static
        self.runStaticLed()
        self.static_player.play(self.static)

    def runStaticLed(self):
        if (self.static_led != None):
            self.static_led.stop()

        self.static_led = staticled.StaticLed(float(self.static) / MAX_STATIC)
        self.static_led.start()

    def handleDial(self, delta):
        if (self.playing):
            if (self.dial_num + delta > MAX_DIAL):
                self.setDial(0)
            elif (self.dial_num + delta > 0):
                self.setDial(self.dial_num + delta)
            else:
                self.setDial(MAX_DIAL)

    def setDial(self, dial):
        self.dial_num = dial
        self.updateChannel(self.dialToChannel(dial))
        self.updateStatic(self.dialToStatic(dial))

    def dialToChannel(self, dial):
        return self.dial_channels[dial]

    def dialToStatic(self, dial):
        return self.dial_static[dial]

    def checkSwitch(self, channel):
        new_playing = GPIO.input(SWITCH_GPIO_IN)
        if (self.playing != new_playing):
            self.setPlaying(new_playing)

    def run(self):
        GPIO.add_event_detect(SWITCH_GPIO_IN,GPIO.RISING,callback=self.checkSwitch)
        self.checkSwitch(None)

        exit = Event()
        try:
            while True:
                exit.wait(60)

        except KeyboardInterrupt:
            self.exit()
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.exit()

    def exit(self):
        self.radio_player.stop()
        self.static_player.stop()

        if (self.text_scroller != None):
            self.text_scroller.stop()

        if (self.static_led != None):
            self.static_led.stop()

if __name__ == '__main__':
    Radio().run()
