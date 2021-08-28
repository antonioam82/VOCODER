import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import style
from tkinter import TclError

style.use('ggplot')

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
    )
x = np.arange(0, 2 * CHUNK, 2)

fig, ax = plt.subplots(1, figsize=(15,7))


line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

plt.show(block=False)

while True:
    data = stream.read(CHUNK)
    data_int = struct.unpack(str(2*CHUNK)+'B',data)
    data_np = np.array(data_int, dtype='b')[::2]+128
    line.set_ydata(data_np)
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        #frame_count += 1
        
    except TclError:
        
        # calculate average frame rate
        #frame_rate = frame_count / (time.time() - start_time)
        
        #print('stream stopped')
        #print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
