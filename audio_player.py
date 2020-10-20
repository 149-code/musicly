from AppKit import NSSound
from Foundation import NSURL
import os, time

class AudioPlayer:
    def __init__(self, filepath, volume = 1):
        if filepath[0] == "/":
            file_url = "file://" + filepath
        else:
            file_url = "file://" + os.path.join(os.getcwd(), filepath)

        ns_url = NSURL.URLWithString_(file_url)

        self.filepath = filepath
        self.ns_sound = NSSound.alloc().initWithContentsOfURL_byReference_(ns_url, True)
        self.ns_sound.setVolume_(volume)

    def elapsed_time(self):
        return self.ns_sound.currentTime()

    def duration(self):
        return self.ns_sound.duration()

    def play(self):
        self.ns_sound.play()

    def stop(self):
        self.ns_sound.stop()

    def pause(self):
        self.ns_sound.pause()

    def resume(self):
        self.ns_sound.resume()
