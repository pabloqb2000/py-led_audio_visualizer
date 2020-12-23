import numpy as np
from utils.to_leds import *
from time import time, sleep

in_file = './npys/song01.npy'
fps = 30

point_values = np.load(in_file)

print(time())
for frame in point_values:
    t1 = time()
    frame_to_leds(frame)
    t = 1/fps - time() + t1
    if t > 0:
        sleep(t)
    else:
        print("WARNING: too fast fps, couldn't change leds in time")

