import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.io import wavfile
from colour import Color
from os import system
from animation_maker import *
from gradient_utils import *
from audio_reader import *

def show_1d_gradient():
    N = 256
    c1, c2 = Color('#01484a'), Color('#fc0b03')

    gradient = list(c1.range_to(c2,256))
    gradient = [c.rgb for c in gradient]

    x = np.linspace(0, 1, N)

    plt.plot(x)
    for i, v in enumerate(x):
        plt.axvline(x=i, color=gradient[int(v*255)])
    plt.show()

def make_fft():
    for i in range(1,3):
        file = f'./Songs/Song0{i}.wav'

        samplerate, data = wavfile.read(file)
        n_samples = data.shape[0]

        print(f"Audio:\n\tSamplerate:\t{samplerate}\n\tFrames:\t\t{n_samples}\n\tDuration:\t{n_samples/samplerate} s")

        data = data/np.max(data)
        volume = np.mean(data, axis=-1)

        mgft = np.abs(np.fft.rfft(volume))
        # mgft = mgft/np.max(mgft)
        xVals = np.fft.rfftfreq(n_samples, d=1/samplerate)

        plt.plot(xVals, mgft)
    plt.legend(["train", "wwry"])
    plt.title("FFT")
    plt.xlabel('Freq')
    plt.show()

def update_line(frame, line, fft_output, freq_range):
    if frame % 100 == 0:
        print (f"{frame} / {len(fft_output)}", end="\r")
    line.set_data(np.array([freq_range, fft_output[frame]]))
    return line,

def make_fft_video():
    file = './Songs/Song02.wav'
    filename = 'lines.mp4'
    fps = 30
    fft_size = 4096*2
    cut = 0.2

    # Get audio data
    samplerate, data = wavfile.read(file)
    data = data[:int(data.shape[0]*cut)]
    n_samples = data.shape[0]
    n_video_frames = int(n_samples/samplerate*fps)

    print(f"Audio:\n\tSamplerate:\t{samplerate}\n\tFrames:\t\t{n_samples}\n\tDuration:\t{n_samples/samplerate} s")

    data = data/np.max(data)
    volume = np.mean(data, axis=-1)

    volume_pad = np.concatenate([np.zeros(int(fft_size/2)), volume, np.zeros(int(fft_size/2))])

    # calculate fft
    fft_input_frames = np.vstack([
        volume_pad[int(i/n_video_frames*n_samples):int(i/n_video_frames*n_samples + fft_size)]
        for i in range(n_video_frames)
    ])
    fft_input_frames = fft_input_frames*np.hanning(fft_size)

    fft_output = np.abs(np.fft.rfft(fft_input_frames))
    fft_output = fft_output/np.max(fft_output)
    freq_range = np.fft.rfftfreq(fft_size, d=1/samplerate)

    print(np.searchsorted(freq_range, 1000))

    # Normalize fft
    fft_output = fft_output / np.power(fft_output.max(0), 1)

    # make animation
    fig1 = plt.figure()
    l, = plt.plot(fft_output[0], freq_range)
    plt.ylim(0, 1)
    plt.xlim(0, 2000)
    plt.xlabel('Freq')
    plt.title('FFT')
    line_ani = animation.FuncAnimation(
        fig1,
        update_line,
        n_video_frames,
        fargs=(l, fft_output, freq_range),
        interval=1000/fps,
        blit=True
    )

    #plt.show()
    line_ani.save(filename)

    print("Adding audio...")
    system('ffmpeg -y -loglevel warning -i ' + filename + ' -i ' + file + ' -c copy -map 0:v:0 -map 1:a:0 ' + filename[:-3] + 'avi')
    system('rm ' + filename)

def update_line_leds(frame, line, fft_output_disc, x_axis):
    if frame % 100 == 0:
        print (f"{frame} / {len(fft_output_disc)}", end="\r")
    line.set_data(np.array([x_axis, fft_output_disc[frame]]))
    return line,

def make_fft_led_video():
    file = './Songs/Song01.wav'
    filename = 'leds.mp4'
    fps = 30
    fft_size = 4096*2
    cut = 0.2
    n_leds = 100
    max_freq = 2000

    # Get audio data
    samplerate, data = wavfile.read(file)
    data = data[:int(data.shape[0]*cut)]
    n_samples = data.shape[0]
    n_video_frames = int(n_samples/samplerate*fps)

    print(f"Audio:\n\tSamplerate:\t{samplerate}\n\tFrames:\t\t{n_samples}\n\tDuration:\t{n_samples/samplerate} s")

    data = data/np.max(data)
    volume = np.mean(data, axis=-1)

    volume_pad = np.concatenate([np.zeros(int(fft_size/2)), volume, np.zeros(int(fft_size/2))])

    # calculate fft
    fft_input_frames = np.vstack([
        volume_pad[int(i/n_video_frames*n_samples):int(i/n_video_frames*n_samples + fft_size)]
        for i in range(n_video_frames)
    ])
    fft_input_frames = fft_input_frames*np.hanning(fft_size)

    fft_output = np.abs(np.fft.rfft(fft_input_frames))
    fft_output = fft_output/np.max(fft_output)
    freq_range = np.fft.rfftfreq(fft_size, d=1/samplerate)

    # Normalize fft
    fft_output = fft_output / np.power(fft_output.max(0), 0.75)

    # Discretize fft
    fft_crop_size = freq_range.searchsorted(max_freq)
    fft_output_disc = fft_output[:,:fft_crop_size]
    _, fft_size = fft_output_disc.shape
    fft_output_disc = fft_output_disc[:,:-(fft_size%n_leds)]
    fft_output_disc = fft_output_disc.reshape((n_video_frames, n_leds, -1)).max(-1)
    print(fft_output_disc.shape)

    # make animation
    fig1 = plt.figure()
    x_axis = np.arange(n_leds)
    l, = plt.step(fft_output_disc[0], x_axis)
    plt.ylim(0, 1)
    plt.xlim(0, n_leds)
    plt.xlabel('LED')
    plt.ylabel('Value')
    plt.title('LED values')
    line_ani = animation.FuncAnimation(
        fig1,
        update_line_leds,
        n_video_frames,
        fargs=(l, fft_output_disc, x_axis),
        interval=1000/fps,
        blit=True
    )

    #plt.show()
    line_ani.save(filename)

    print("Adding audio...")
    system('ffmpeg -y -loglevel warning -i ' + filename + ' -i ' + file + ' -c copy -map 0:v:0 -map 1:a:0 ' + filename[:-3] + 'avi')
    system('rm ' + filename)

def volume_plot():
    fps = 30
    start, end = 10, 20
    l = end - start
    data, conv, disc_conv, info = get_volume('./Songs/Song02.wav', ksize=2000, normalize=True, fps=fps)
    samplerate, frames = info

    for xc in np.linspace(start, end, fps*l):
        plt.axvline(x=xc, color=(0.8, 0.8, 0.8), linewidth=0.5, linestyle="--")

    disc_conv = np.repeat(disc_conv, int(samplerate/fps))
    x = np.linspace(start, end, samplerate*l)
    plt.plot(x, data[start*samplerate:end*samplerate], linestyle="-")
    plt.plot(x, conv[start*samplerate:end*samplerate], linewidth=2)
    plt.plot(x, disc_conv[start*samplerate:end*samplerate], linewidth=2)
    
    plt.legend(["Ch 1", "Ch 2", "Convolution", "Video vol"])
    plt.title("Linear convulution for volume")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume")
    plt.show()

def show_2d_grad(c1, c2, c3, c4, mode='hsl-l', n=256):
    cols = get_gradient_2d(c1, c2, c3, c4, mode, n)
    print(cols.shape)
    plt.imshow(cols/255)
    plt.show()


show_2d_grad(Color('#fceaa8'), Color('#00e5ff'), Color('#000000'), Color('#000000'))