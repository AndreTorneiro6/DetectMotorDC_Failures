import socket
import pickle
import pyaudio
import threading
import numpy as np
from audio import audio_features
import time


localIP = "192.168.0.11"
localPort = 8000
bufferSize = 8192
message = ''
address = ''

# audio variables
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 22050  # Record at 44100 samples per second
frames = []  # Initialize array to store frames
p = pyaudio.PyAudio()  # Create an interface to PortAudio
status = True


def client_listener():
    global message
    global address
    global status
    while True:
        bytes_address_pair = host_socket.recvfrom(bufferSize)
        message = bytes_address_pair[0].decode()
        address = bytes_address_pair[1]
        print(message)
        if message == 'Stop':
            status = False
        if message == 'Begin':
            status = True


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as host_socket:
    global stream
    try:
        host_socket.bind((localIP, localPort))

        print('Starting listener thread...')
        listener_thread = threading.Thread(target=client_listener)
        listener_thread.daemon = True
        listener_thread.start()
        print('Listener thread started!')
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        while True:
            data = stream.read(chunk)
            frames.append(np.frombuffer(data, dtype=np.int16))
            if message == 'Begin':
                host_socket.sendto(pickle.dumps([1]), address)
                message = ''
            if message == 'Get':
                message = ''
                features = audio_features(np.hstack(frames))
                data_to_send = pickle.dumps(list(features))
                print(data_to_send)
                frames.clear()
                # Sending a reply to client
                host_socket.sendto(data_to_send, address)
                # host_socket.sendto(pickle.dumps([1]), address)
            if message == 'Stop':
                host_socket.sendto(pickle.dumps([0]), address)
                message = ''
        # else:
        #     # Stop and close the stream
        #     # stream.stop_stream()
        #     # stream.close()
        #     # # Terminate the PortAudio interface
        #     # p.terminate()
        #     frames.clear()
        #     if message == 'Stop':
        #         host_socket.sendto(pickle.dumps([0]), address)
        #     while not status:
        #         continue

    except socket.error as error:
        host_socket.close()

# localIP = "192.168.0.11"
#
# localPort = 8000
#
# bufferSize = 4096
#
# # Create a datagram socket
#
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#
# # Bind to address and ip
#
# UDPServerSocket.bind((localIP, localPort))
#
# print("UDP server up and listening")

# Listen for incoming datagrams
# while True:
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#
#     message = bytesAddressPair[0].decode()
#
#     address = bytesAddressPair[1]
#     print(message)
#     if message == 'Begin':
#         UDPServerSocket.sendto(pickle.dumps([1]), address)
#         # record_audio(message)
#     elif message == 'Get':
#         # data_to_send = pickle.dumps(record_audio(message))
#         # Sending a reply to client
#         # UDPServerSocket.sendto(data_to_send, address)
#         UDPServerSocket.sendto(pickle.dumps([1]), address)
#     else:
#         UDPServerSocket.sendto(pickle.dumps([1]), address)
#         # record_audio(message)
#
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP = "Client IP Address:{}".format(address)
#
#     print(clientMsg)
#     print(clientIP)
# import pyaudio
# host = socket.gethostbyname(socket.gethostname())
# port = 8000
# # buffer = 2048
# clients = []
#
# # Audio
# audio = pyaudio.PyAudio()
# chunk = int(1024 * 4)
#
#
# def client_listener():
#     while True:
#         data, address = host_socket.recvfrom(bufferSize)
#         if address not in clients:
#             print(f'New client: {address[0]}:{address[1]}')
#             clients.append(address)
#             print(clients)
#
#
# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as host_socket:
#     try:
#         host_socket.bind((localIP, localPort))
#         print(f'Server hosted at {host}:{port}\n')
#
#         print('Starting listener thread...')
#         listener_thread = threading.Thread(target=client_listener)
#         listener_thread.daemon = True
#         listener_thread.start()
#         print('Listener thread started!')
#
#         print('Initiating microphone...')
#         stream = audio.open(format=pyaudio.paInt16,
#                             channels=1,
#                             rate=44100,
#                             input=True,
#                             frames_per_buffer=chunk)
#
#         print('Recording!')
#         while True:
#             voice_data = stream.read(chunk, exception_on_overflow=False)
#             for client in clients:
#                 host_socket.sendto(voice_data, client)
#     except socket.error as error:
#         print(str(error))
#         stream.close()
#         host_socket.close()
#     except KeyboardInterrupt:
#         stream.close()
#         host_socket.close()
#     finally:
#         stream.close()
#         host_socket.close()
