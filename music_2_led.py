from colour import Color
from to_leds import *
from animation_maker import *
from time import time, sleep

in_file = './Songs/Song02.wav'
c1, c2 = Color('#fceaa8'), Color('#00e5ff')
#c1, c2 = Color('#000000'), Color('#00fffb')
c3, c4 = Color('#000000'), Color('#000000')
gradient_mode = 'hsl'
n_points = 100
# anim_mode = 'fft 2000 8192 1'
anim_mode = 'volume_bar bounce'
fps = 30

point_values = make_animation(in_file, anim_mode, n_points, fps, c1, c2, c3, c4, gradient_mode)

print(time())
for frame in point_values:
    t1 = time()
    frame_to_leds(frame)
    sleep(1/fps - time() + t1)

