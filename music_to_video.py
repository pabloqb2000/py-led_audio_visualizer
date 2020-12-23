from colour import Color
from utils.video_maker import *
from utils.animation_maker import *

in_file = './Songs/Song02.wav'
c1, c2 = Color('#fceaa8'), Color('#00e5ff')
#c1, c2 = Color('#000000'), Color('#00fffb')
c3, c4 = Color('#000000'), Color('#000000')
gradient_mode = 'hsl'
n_points = 100
anim_mode = 'fft 2000 8192 1'
fps = 30

h,w,bg = 1020, None, 20
out_file = './videos/test.mp4' # will still be a .avi file

point_values = make_animation(in_file, anim_mode, n_points, fps, c1, c2, c3, c4, gradient_mode)

video = create_animation(point_values, h, w, bg)

create_video_file(video, out_file, in_file, fps, transpose=True)


