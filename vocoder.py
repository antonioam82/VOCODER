from tkinter import *
import pyaudio
import numpy as np
import threading
import time

class vocod():
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("200x200")
        self.channels = 2
        self.rate = 44100
        self.p = pyaudio.PyAudio()
        self.active = False

        Button(self.ventana,text="START",command=self.init_task).place(x=100,y=100)
        Button(self.ventana,text="CLOSE",command=self.close_stream).place(x=100,y=160)

        
        self.ventana.mainloop()

    def callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.fromstring(in_data, dtype=np.float32)#fromstring
        x = np.linspace(0, np.pi*2, audio_data.shape[0])
        fundamental = np.sin(x*5)
        audio_data *= fundamental

        return audio_data.astype(np.float32), pyaudio.paContinue

    def listening(self):
        self.stream = self.p.open(
            format = pyaudio.paFloat32,
            channels = self.channels,
            rate = self.rate,
            output = True,
            input = True,
            stream_callback=self.callback,
            )
        self.active = True
        self.stream.start_stream()

    def init_task(self):
        t = threading.Thread(target=self.listening)
        t.start()

    def close_stream(self):
        if self.active == True:
            self.stream.close()
            self.active = False

if __name__=="__main__":
    vocod()
