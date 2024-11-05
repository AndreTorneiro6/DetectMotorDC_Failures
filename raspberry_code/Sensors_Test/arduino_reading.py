import serial
import time
import schedule

def main_func():
    arduino_connection = serial.Serial('/dev/ttyUSB1', 115200)
    
    arduino_data = arduino_connection.readline()
    
    decoded_values = str(arduino_data[0:len(arduino_data)].decode('utf-8')).strip()
    print(decoded_values)
    
    arduino_connection.close()
    
    return decoded_values
    
schedule.every(1).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)
    
    