#!/usr/bin/python
import sys, select, traceback, math
import mpcplaylistplayer, staticplayer, playlist

PLAYLIST_NAME = 'radio'
MAX_STATIC = 5

class Radio:
    radio_player = None
    static_player = None
    playlist = None

    dial_num = 0
    dial_channels = [];
    dial_static = [];

    def __init__(self):
        self.playlist = playlist.Playlist(PLAYLIST_NAME)
        self.radio_player = mpcplaylistplayer.MpcPlaylistPlayer()
        self.static_player = staticplayer.StaticPlayer()
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
        print self.playlist.getChannelName(self.channel)

    def setDial(self, dial):
        self.dial_num = dial
        self.channel = self.dialToChannel(dial)
        self.static = self.dialToStatic(dial)
        self.radio_player.playChannel(self.channel)
        self.static_player.play(self.static)
        self.printChannelName()

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
                        self.radio_player.exit()
                        sys.exit()
        except KeyboardInterrupt:
            self.exit()
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.exit()

    def exit(self):
        self.radio_player.stop()
        self.static_player.stop()

if __name__ == '__main__':
    Radio().run()
