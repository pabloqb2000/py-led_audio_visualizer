from colour import Color
from video_maker import *
from animation_maker import *

in_file = './Songs/Song01.wav'
c1, c2 = Color('#fceaa8'), Color('#00e5ff')
#c1, c2 = Color('#000000'), Color('#00fffb')
c3, c4 = Color('#000000'), Color('#000000')
gradient_mode = 'hsl'
n_points = 100
anim_mode = 'fft 2000 8192 1'
fps = 30

out_file = './npys/song01.npy' # will still be a .avi file

point_values = make_animation(in_file, anim_mode, n_points, fps, c1, c2, c3, c4, gradient_mode)

np.save(out_file, point_values)