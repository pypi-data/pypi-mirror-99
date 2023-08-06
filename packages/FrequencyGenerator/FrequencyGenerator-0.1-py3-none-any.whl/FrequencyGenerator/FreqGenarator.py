# Gobal Krishnan V
import numpy
import pyaudio
import math
from tkinter import *
import webbrowser
import os

#from tkinter.ttk import *
class ToneGenerator(object):
    def __init__(self, samplerate = 44100, frames_per_buffer = 4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False

    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            xs = numpy.arange(self.buffer_offset,self.x_max)  
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset, self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer 
        return out

    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(),pyaudio.paContinue) 
        else:
            return (None, pyaudio.paComplete)

    def is_playing(self):
        if self.stream.is_active():
            return True 
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False 
            return False 
    
    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate 
        self.amplitude = amplitude 
        self.buffer_offset  = 0 
        self.streamOpen = True 
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format = pyaudio.paFloat32,
                                channels = 1,
                                rate = self.samplerate,
                                output = True,
                                frames_per_buffer = self.frames_per_buffer,
                                stream_callback = self.callback)
                                                             
        
def play(freq,step_duration,amplitude):
    generator.play(freq,step_duration,amplitude)
    while generator.is_playing():
      pass

generator = ToneGenerator()

frequency_start  = 50
frequency_end    = 10000
num_frequency    = 5
amplitude        = 0.1
step_duration    = 30

"""
play(396,step_duration,amplitude)
play(417,step_duration,amplitude)
play(528,step_duration,amplitude)
play(639,step_duration,amplitude)
play(741,step_duration,amplitude)
play(852,step_duration,amplitude)
play(963,step_duration,amplitude)
"""





"""
for frequency in numpy.logspace(math.log(frequency_start,10),math.log(frequency_end,10),num_frequency):
    print("Playing tone at {0:0.2f} Hz".format(frequency))
    while generator.is_playing():
        pass
"""

"""
import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio     #initialize pyaudio
BITRATE = 5000     #number of frames per second/frameset.
FREQUENCY = 10000     #Hz, waves per second, 261.63=C4-note.
LENGTH = 5    #seconds to play sound
if FREQUENCY > BITRATE:
   BITRATE = FREQUENCY+100
NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''
#generating waves
for x in range(NUMBEROFFRAMES):
     WAVEDATA =
WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))
for x in range(RESTFRAMES):
    WAVEDATA = WAVEDATA+chr(128)
print(WAVEDATA)
p = PyAudio()
stream = p.open(format = p.get_format_from_width(1),channels =     2,rate = BITRATE,output = True)
stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()
"""

frame = Tk()
frame.title("Frequency Generator")

#logo = PhotoImage(r'F:/audio/seed.png')
#frame.iconphoto(False,logo)
#frame.iconphoto(False, 'F:/audio/seed.png')
#frame.iconphoto(False, PhotoImage(file='F:/audio/seed1.png'))
#print(a)
#
a = os.getcwd()
path = a+'\src\FrequencyGenerator\seed1.ico'
print(path)
if(os.path.exists(path)):
    
      frame.iconbitmap(path)

"""
This application is made using Gobal Krishnan V
link = http://engineer-ece.github.io/Home n
"""
n0= StringVar()
n1= StringVar()
n2= StringVar()

def callback(url):
    webbrowser.open_new(url)

l_link = Label(frame, text="http://engineer-ece.github.io/Home",fg="blue", cursor="hand2")
l_link.bind("<Button-1>",lambda e: callback("http://engineer-ece.github.io/Home"))

l_link.pack(side = TOP)

l_freq = Label(frame, text="Frequency")
l_freq.pack(side = LEFT)

e_freq = Entry(frame,textvariable = n0, bd= 5)
e_freq.pack(side = LEFT)

l_amplitude = Label(frame, text="Volume")
l_amplitude.pack(side = LEFT)

e_amplitude = Entry(frame,textvariable = n1, bd= 5)
e_amplitude.pack(side = LEFT)

l_stepDuration = Label(frame, text="Time")
l_stepDuration.pack(side = LEFT)

e_stepDuration = Entry(frame,textvariable = n2, bd= 5)
e_stepDuration.pack(side = LEFT)



def fplay():
    fre = float(n0.get())
    amp = float(n1.get())
    dur = int(n2.get())
    play(fre,dur,amp)
    

b_play = Button(frame, text="play", command = fplay)
b_play.pack(side=LEFT)



frame.mainloop()