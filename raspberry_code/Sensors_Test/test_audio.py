import serial
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.io.wavfile import write
import wave
import struct

def audnorm(aud):
    normaud=  -1+2*((aud-np.amin(aud))/(np.amax(aud)-np.amin(aud)))
    return normaud


sound=[]
arduino_connection = serial.Serial('/dev/ttyUSB0', 115200)

try:
    while True:
         if arduino_connection.in_waiting > 0:
            arduino_data = arduino_connection.readline()
            try:
                decoded_values = str(arduino_data[0:len(arduino_data)].decode('utf-8')).rstrip()
            except ValueError:
                raise InputError('got bad value {}'.format(decoded_values))
            
            print(decoded_values)
            sound.append(int(decoded_values))
except KeyboardInterrupt:
    arduino_connection.close()

    soundnp= np.asarray(sound)

    soundnp= soundnp - np.mean(soundnp)


    soundnorm= audnorm(soundnp)

    soundnormstr= [x for x in soundnorm]
    

    plt.plot(soundnp)
    plt.show()

    plt.plot(soundnorm)
    plt.show()

    write('a.wav',16000,soundnormstr)

