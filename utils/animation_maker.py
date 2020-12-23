import numpy as np
from colour import Color
from utils.audio_reader import *
from utils.gradient_utils import *

'''
    Creates an animation based on the animation mode string
    Given:
        - in_file: .wav file to read from
        - anim_mode: the animation command, choose from:
            · volume_bar [sim] [bounce]
            · volume_beam [pow]
            · volume_full_bar [pow]
            · fft [max_freq] [fft_size] [norm_value]
        - n_points: the number of points to color
        - fps: fps of the output animation
        - c1, c2, c3, c4: colors for the gradients (determines the color of the output)
        - gradient_mode: mode of interpolation of the gradient
    Returns a numpy array with shape (f, n, 3)
        - f: for the number of frames
        - n: for the number of points (leds)
        - 3: for the rgb channels
        The colors are encoded in the 0-255 RGB format
'''
def make_animation(in_file, anim_mode, n_points, fps, c1, c2, c3=Color('#000000'), c4=Color('#000000'), gradient_mode='hsl'):
    if anim_mode.startswith('volume'):
        gradient = get_gradient_1d(c1, c2, mode=gradient_mode)

        data, conv, disc_conv, info = get_volume(in_file, fps=fps)
        samplerate, n_samples = info
        n_frames = len(disc_conv)

        point_values = get_points_colors_volume(
            disc_conv,
            n_frames,
            n_points,
            gradient,
            anim_mode=anim_mode,
        )
    elif anim_mode.startswith('fft'):
        command = anim_mode.split(' ')

        fft_output, fft_leds, info = get_fft(
            in_file,
            fps,
            n_points,
            int(command[1]),
            int(command[2]),
            float(command[3])
        )
        samplerate, n_samples = info
        n_frames = len(fft_leds)

        point_values = get_points_colors_fft(fft_leds, c1, c2, c3, c4, gradient_mode)
    else:
        print("NOT VALID COMMAND!")
        return None
        
    return point_values

'''
    Makes an animation based on the fft of the signal
    Given:
        - fft_output_leds: the discretized fft for the leds
        - c1, c2, c3, c4: the colors to use
        - gradient_mode: the type of 2D gradient
    Returns a numpy array with shape (f, n, 3)
        - f: for the number of frames
        - n: for the number of points (leds)
        - 3: for the rgb channels
        The colors are encoded in the 0-255 RGB format
'''
def get_points_colors_fft(fft_output_leds, c1, c2, c3=Color('#000000'), c4=Color('#000000'), gradient_mode='hsl'):
    grad_2d = np.array(get_gradient_2d(c1, c2, c3, c4, gradient_mode), dtype='uint8')
    n_frames, n_leds = fft_output_leds.shape

    # Led normalization
    min_led, max_led = np.min(fft_output_leds, axis=-1), np.max(fft_output_leds, axis=-1)
    diff_led = max_led - min_led
    diff_led[diff_led == 0] = 1
    fft_output_leds = ((fft_output_leds.T - min_led) / (diff_led)).T

    fft_output_leds = np.floor(fft_output_leds*255).astype(int)
    
    point_values = np.array([
        [
            grad_2d[255-led][int(i/n_leds*255)]
            for i, led in enumerate(frame)
        ]
        for frame in fft_output_leds
    ])
    
    return point_values


'''
    Makes an animation based on the volume of the signal
    Given:
        - signal: the volume signal
        - n_frames: the number of frames to output
        - n_points: the number of points to color
        - gradient: the gradient of colors to choose from
        - anim_mode: the animation command, choose from:
            · volume_bar [sim] [bounce] // sim for simmetric animation and ball for a bouncing ball
            . volume_beam [pow] // power to use on volume interpolation
            . volume_full_bar [pow] // power to use on volume interpolation
    Returns a numpy array with shape (f, n, 3)
        - f: for the number of frames
        - n: for the number of points (leds)
        - 3: for the rgb channels
        The colors are encoded in the 0-255 RGB format
'''
def get_points_colors_volume(signal, n_frames, n_points, gradient, anim_mode='volume_bar', simetric=False, bounce_ball=True):
    command = anim_mode.split(' ')
    if command[0] == 'volume_bar':
        return volume_bar_animation(
            signal,
            n_frames,
            n_points,
            gradient,
            'sim' in anim_mode,
            'ball' in anim_mode or 'bounce' in anim_mode
        )
    elif command[0] == 'volume_beam':
        return volume_beam_animation(
            signal,
            n_frames,
            n_points,
            gradient,
            float(command[1])
        )
    elif command[0] == 'volume_full_bar':
        return volume_full_bar_animation(
            signal,
            n_frames,
            n_points,
            gradient,
            float(command[1])
        )
    else:
        print("NOT VALID COMMAND!")
        return None

'''
    Returns the numpy array
    for the volume_full_bar animation
'''
def volume_full_bar_animation(signal, n_frames, n_points, gradient, pow=1):
    point_values = np.zeros((n_frames, n_points, 3))
    grad_size = len(gradient) - 1

    for vol, points in zip(signal, point_values):
        color = gradient[int(np.power(vol, pow)*grad_size)]
        points[:] = np.tile(color, (n_points, 1))
    
    return point_values

'''
    Returns the numpy array
    for the volume_beam animation
'''
def volume_beam_animation(signal, n_frames, n_points, gradient, pow=1):
    point_values = np.zeros((n_frames, n_points, 3))
    grad_size = len(gradient) - 1

    for i, vol in enumerate(signal):
        last_frame = point_values[i-1]
        frame = point_values[i]
        frame[1:] = last_frame[:-1]
        frame[0] = gradient[int(np.power(vol, pow)*grad_size)]

    return point_values

'''
    Returns the numpy array
    for the volume_bar animation
'''
def volume_bar_animation(signal, n_frames, n_points, gradient, simetric, bounce_ball):
    point_values = np.zeros((n_frames, n_points, 3))
    grad_size = len(gradient) - 1
    bounce = 0

    if not simetric:
        for vol, points in zip(signal, point_values):
            bar_size = int(np.round(vol*n_points))
            color = gradient[int(vol*grad_size)]
            points[:bar_size] = np.tile(color, (bar_size, 1))
            if bounce_ball:
                if bounce < bar_size:
                    bounce = bar_size - 1
                else:
                    bounce -= 1
                points[bounce] = color
                    
    else: 
        for vol, points in zip(signal, point_values):
            bar_size = int(np.floor(vol*n_points/2))
            start = int(n_points/2)
            color = gradient[int(vol*grad_size)]
            vals = np.tile(color, (bar_size, 1))
            points[start:start + bar_size] = vals
            points[start-bar_size:start] = vals[::-1]
            if bounce_ball:
                if bounce < bar_size:
                    bounce = bar_size - 1
                else:
                    bounce -= 1
                points[start + bounce] = color
                points[start - bounce] = color

    return point_values
    


