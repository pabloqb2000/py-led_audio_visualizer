from scipy.io import wavfile
import numpy as np

'''
    Given:
        - file: a .wav file
        - ksize: size of kernels to take the volme mean from
        - nomralize: whether to normalize the signal
        - fps: fps of the discretized output
    Rerturns:
        - The channels data in the file
        - A volume signal
        - The volume signal averaged for each frame given the fps
        - Info tuple with:
            · Sample rate in the file
            · Audio samples in the file
'''
def get_volume(file, ksize=2000, normalize=True, fps=30):
    samplerate, data = wavfile.read(file)
    n_samples = data.shape[0]

    print(f"Audio:\n\tSamplerate:\t{samplerate}\n\tFrames:\t\t{n_samples}\n\tDuration:\t{n_samples/samplerate} s")

    data = data/np.max(data)
    volume = np.mean(np.absolute(data), axis=-1)

    ker = np.hanning(ksize + 1)
    t = int(ksize/2)
    conv = np.convolve(volume,ker)[t:-t]
    if normalize:
        conv = conv/np.max(conv)

    samples_per_frame = int(samplerate/fps)
    # disc_conv = conv[::t]
    disc_conv = np.mean(conv[:-(n_samples%samples_per_frame)].reshape(-1, samples_per_frame), axis=1)
    if normalize:
        disc_conv = disc_conv/np.max(disc_conv)

    return data, conv, disc_conv, (samplerate, n_samples)

'''
    Given:
        - file: a .wav file
        - fps: fps of the discretized output
        - n_leds: n_leds of the discretized output
        - max_freq: max frequency cut
        - fft_size: number of samples input to the fft
        - norm_value: normalization factor (0: no normalization, 1: full)
    Rerturns:
        - The output of the fft
        - The discretized output for the number of leds
        - Info tuple with:
            · Sample rate in the file
            · Audio samples in the file
'''
def get_fft(file, fps=30, n_leds=100, max_freq=2000, fft_size=8192, norm_value=0.75):
    # Get audio data
    samplerate, data = wavfile.read(file)
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
    fft_output = fft_output / np.power(fft_output.max(0), norm_value)

    # Discretize fft
    fft_crop_size = freq_range.searchsorted(max_freq)
    fft_output_disc = fft_output[:,:fft_crop_size]
    _, fft_size = fft_output_disc.shape
    fft_output_disc = fft_output_disc[:,:-(fft_size%n_leds)]
    fft_output_disc = fft_output_disc.reshape((n_video_frames, n_leds, -1)).max(-1)

    return fft_output, fft_output_disc, (samplerate, n_samples)