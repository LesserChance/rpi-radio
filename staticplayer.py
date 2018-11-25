#!/usr/bin/python
import subprocess

ASSET_DIR = "./assets/"

class StaticPlayer:
    current_static = None
    sp = None

    def __init__(self):
        self.stop()

    def on(self):
        self.forcePlay(self.current_static)

    def off(self):
        self.stop()

    def stop(self):
        try:
            self.sp.terminate()
        except Exception:
            pass

    def play(self, new_static):
        if (new_static != self.current_static):
            self.forcePlay(new_static)

    def forcePlay(self, new_static):
            self.current_static = new_static
            self.stop()
            if (new_static > 0):
                self.playStatic(self.current_static)

    def playStatic(self, static_file):
        self.sp = subprocess.Popen(["aplay", "-q", ASSET_DIR + "whitenoise-" + str(static_file) + ".wav"])
