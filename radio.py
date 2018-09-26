#!/usr/bin/python
import sys, select, traceback, math
import mpcplaylistplayer, staticplayer, playlist, textscroller, staticled, rotary

PLAYLIST_NAME = 'radio'
MAX_STATIC = 5

DIAL_GPIO_A = 17
DIAL_GPIO_B = 18

class Radio:
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

    def generateDialArrays(self):
        spacing = int(255 / self.playlist.getChannelCount())
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
        if (self.dial_num + delta > 0):
            self.setDial(self.dial_num + delta)

    def setDial(self, dial):
        self.dial_num = dial
        self.updateChannel(self.dialToChannel(dial))
        self.updateStatic(self.dialToStatic(dial))

    def dialToChannel(self, dial):
        return self.dial_channels[dial]

    def dialToStatic(self, dial):
        return self.dial_static[dial]

    def run(self):
        self.start()

        try:
            timeout = 10
            while True:
                rlist, _, _ = select.select([sys.stdin], [], [], timeout)
                if rlist:
                    key = sys.stdin.readline().replace('\n', '')
                    if key == 'u':
                        self.setDial(self.dial_num + 1)
                    if key == 'd':
                        self.setDial(self.dial_num - 1)
                    if key == 'x':
                        self.exit()
                        sys.exit()
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
