# Taken from https://forum.cogsci.nl/index.php?p=/discussion/1772/ 
# and https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
import pyaudio
import struct
import math 
import time
import csv

# A low threshold increases sensitivity, a high threshold reduces it.
sound_threshold = 20
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 48000
chunk=1024
swidth = 2

class Detector:

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.vol = []
    
    def __del__(self):
        self.p.terminate()

    def __rms(self, frame):
            count = len(frame) / swidth
            format = "%dh" % (count)
            shorts = struct.unpack(format, frame)
            sum_squares = 0.0
            for sample in shorts:
                n = sample * SHORT_NORMALIZE
                sum_squares += n * n
            rms = math.pow(sum_squares / count, 0.5)
            return rms * 1000

    def __listen(self, timeout, thresh=sound_threshold):
        stream = self.p.open(       # Open sound stream
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=1,
        frames_per_buffer=chunk
        )
        start_time = time.time()
        print("Listening...")
        while True:
            sound_in = stream.read(chunk)
            loudness = self.__rms(sound_in)
            if time.time() - start_time >= timeout:
                stream.close()
                return float("NaN")
            if loudness > thresh:
                response_time = time.time() - start_time
                print("Caught sound!")
                stream.close()
                return response_time
    
    def record_vol(self, timeout, thresh = sound_threshold):
        self.vol.append(self.__listen(timeout))
    
    def to_csv(self, filename, in_milliseconds = False):
        with open(filename, 'a', newline='') as csv_file:
            csvwriter = csv.writer(csv_file)
            if in_milliseconds == True:
                csvwriter.writerow([item * 1000 for item in self.vol])
            else:
                csvwriter.writerow(self.vol)
    
    def test_mic(self):
        print("Say something!")
        if self.__listen(timeout=5) == None:
            print("Couldn't detect any input. Check that your microphone is selected and connected!")
        else:
            print("Input detected!")