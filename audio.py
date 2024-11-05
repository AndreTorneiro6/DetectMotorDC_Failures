import pyaudio
import numpy as np
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from librosa import feature, magphase, stft
import matplotlib.pyplot as plt


def filter_audio(audio_content, fs = 22050):
    # nyquist frequency
    nyq = 0.5 * fs

    # normalize cutoff frequency
    low = 4000 / nyq
    high = 9000 / nyq

    # define 5th order band-pass butterworth filter
    b, a = butter(5, [low, high], btype='band')

    # set initial state of the filter
    zi = lfilter_zi(b, a)

    # filter signal from left to right
    z, _ = lfilter(b, a, audio_content, zi=zi * audio_content[0])

    # filter signal from right to left
    z2, _ = lfilter(b, a, z, zi=zi * z[0])

    # filter signal forward and backward
    audio_filtered = filtfilt(b, a, audio_content)

    return audio_filtered


def audio_features(audio_content):
    filtered_audio = filter_audio(audio_content)
    stft_signal, _ = magphase(stft(filtered_audio))
    features = feature.rms(S=stft_signal)[0]
    # plt.plot(features)
    # plt.show()

    return features


stream = None


def record_audio(status):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 22050  # Record at 44100 samples per second
    frames = []  # Initialize array to store frames
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    global stream
    if status == 'Begin':
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        while True:
            print('Recording...')
            data = stream.read(chunk)
            frames.append(np.frombuffer(data, dtype=np.int16))
    elif status == 'Get':
        # Convert the list of numpy-arrays into a 1D array (column-wise)
        return np.hstack(frames)

    else:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
    # # Store data in chunks for 3 seconds
    # for i in range(0, int(fs / chunk * seconds)):
    #     data = stream.read(chunk)
    #     frames.append(np.frombuffer(data, dtype=np.int16))
    #
    # # Convert the list of numpy-arrays into a 1D array (column-wise)
    # numpydata = np.hstack(frames)

    # fig = plt.figure()
    # s = fig.add_subplot(111)
    # s.plot(numpydata)
    # plt.show()

    print('Finished recording')

    # # Save the recorded data as a WAV file
    # wf = wave.open(filename, 'wb')
    # wf.setnchannels(channels)
    # wf.setsampwidth(p.get_sample_size(sample_format))
    # wf.setframerate(fs)
    # wf.writeframes(b''.join(frames))
    # wf.close()


