# from sensors_connectivity import SensorsReading, MotorControl
# import time
#
# # initialize values for reading sensors
# initialized_values = {'velocity_gpio': 21, 'motor_slots': 40, 'slots_counted':0,'rpm': 0,
#                       'object_temp': 0,'ambient_temp': 0,'acc_measurement': 0, 'gyro_measurement': 0,
#                       'start_time': time.time() }
#
# # pass initialized values to SensorsReading class
# read = SensorsReading(**initialized_values)
#
# # activate gpio's setup
# read.gpio_setup()
#
# # instance of motor control class with duty_cycle = 0
# motor = MotorControl(velocity=100)
#
# # activate initial setup
# motor.gpio_setup()
# motor.control_velocity = 0
# motor.start_motor()
#
# try:
#     while True:
#         read.get_all_readings()
#         # motor.start_motor()
#         """motor.control_velocity = int(input('Entre com o Ciclo de Trabalho -> 0 a 100: '))
#         if motor.control_velocity == 50:
#             motor.stop_motor()
#             motor.turnOff_motor()"""
#         #aa()
#         #time.sleep(0.1)
#         """print (read.rpm_value)
#         print(read.acceleration)
#         print(f'{read.ambient_temperature} / {read.object_temperature}')
#         print(read.counted_motor_slots)"""
#
# except KeyboardInterrupt:
#     motor.stop_motor()
#     motor.turnOff_motor()
#     read.stop_and_clean_reading()

# import socket
#
# msgFromClient = "Hello UDP Server"
#
# bytesToSend = str.encode(msgFromClient)
#
# serverAddressPort = ("192.168.0.10", 20001)
#
# bufferSize = 1024
#
# # Create a UDP socket at client side
#
# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#
# # Send to server using created UDP socket
#
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)
#
# msgFromServer = UDPClientSocket.recvfrom(bufferSize)
#
# msg = "Message from Server {}".format(msgFromServer[0])
#
# print(msg)

import socket
import pickle

localIP = "192.168.0.11"

localPort = 8000

bufferSize = 4096

msgFromServer = [0,'a',False]
MESSAGE = pickle.dumps(msgFromServer)
bytesToSend = str(msgFromServer).encode()

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)


    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(MESSAGE, address)