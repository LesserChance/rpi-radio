#!/usr/bin/python
PLAYLIST_DIR = '/var/lib/mpd/playlists/'

class Playlist:
    playlist_name = None
    channels = []

    def __init__(self, name):
        self.playlist_name = name

        # load the file
        fh = open(PLAYLIST_DIR + name + '.m3u','r')
        load_channels = []
        for playlist_file in fh.readlines():
            channel_name = playlist_file.split('#')[1].replace('\n', '').strip()
            self.channels.append(channel_name);

    def getName(self):
        return self.playlist_name

    def getChannelName(self, channel):
        return self.channels[channel]

    def getChannelCount(self):
        return len(self.channels)
