#!/usr/bin/python3
import shlex, subprocess

class MpcPlaylistPlayer:
    playlist = None
    current_channel = None

    def __init__(self):
        self.stop

    def on(self):
        self.mpc('toggle')

    def off(self):
        self.mpc('toggle')

    def start(self, playlist):
        self.playlist = playlist
        self.mpc('clear')
        self.mpc('volume 90')
        self.mpc('load ' + self.playlist.getName())

    def stop(self):
        self.mpc('stop')

    def playChannel(self, new_channel):
        if (new_channel >= self.playlist.getChannelCount()):
            # handle the backward looping behavior
            new_channel = 0

        new_channel = new_channel + 1 # mpc channels are 1-based
        if (new_channel != self.current_channel):
            self.current_channel = new_channel
            self.mpc('play ' + str(new_channel))

    def mpc(self, cmd):
        cmd = 'mpc ' + cmd
        result = subprocess.check_output(
            shlex.split(cmd), stderr=subprocess.STDOUT
        )
        result = result.decode("utf-8").rstrip().split("\n")
        return result
