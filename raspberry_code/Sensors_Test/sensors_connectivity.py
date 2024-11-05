# required imports
from __future__ import print_function
import RPi.GPIO as GPIO
import time
from smbus2 import SMBus
from mlx90614 import MLX90614
from mpu6050 import mpu6050
import serial

class SensorsReading:
    
    def __init__(self,**kwargs):
        self.rpm_gpio = kwargs['velocity_gpio']
        self.rpm_value = kwargs['rpm']
        self.object_temperature = kwargs['object_temp']
        self.ambient_temperature = kwargs['ambient_temp']
        self.acceleration = kwargs['acc_measurement']
        self.gyroscope_data = kwargs['gyro_measurement']
        self.motor_slots = kwargs['motor_slots']
        self.counted_motor_slots= kwargs['slots_counted']
        self.start_time_rpm_reading = kwargs['start_time']
        self.audio_value = None
        self.arduino_connection = None
        

    def gpio_setup(self):
        # set gpio configuration to use default gpio board configuration
        GPIO.setmode(GPIO.BCM)

        # set ir_gpio as input
        # GPIO.setup(self.ir_gpio, GPIO.IN)

        # set velocity_gpio as input and pull-up configuration
        GPIO.setup(self.rpm_gpio, GPIO.IN)
        GPIO.setup(self.rpm_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # create interruption for velocity_gpio
        GPIO.add_event_detect(self.rpm_gpio, GPIO.FALLING, bouncetime=15)
        
        # create instance for mpu sensor
        #self.mpu = mpu6050(0x68)
        
        # create instance for thermometer sensor
        self.thermometer = MLX90614(SMBus(1), address=0x5A)
        
        # create connection to read arduino
        #self.arduino_connection = serial.Serial('/dev/ttyUSB0', 115200)


    def read_accelerometer(self):
        self.acceleration = self.mpu.get_accel_data()
        self.gyroscope_data = self.mpu.get_gyro_data()

        #print(f'accelerometer = {self.acceleration} \n gyroscope = {self.gyroscope_data}')
            # print("Temp : " + str(mpu.get_temp()))
            # print()
            #
            # accel_data = mpu.get_accel_data()
            # print("Acc X : " + str(accel_data['x']))
            # print("Acc Y : " + str(accel_data['y']))
            # print("Acc Z : " + str(accel_data['z']))
            # print()
            #
            # gyro_data = mpu.get_gyro_data()
            # print("Gyro X : " + str(gyro_data['x']))
            # print("Gyro Y : " + str(gyro_data['y']))
            # print("Gyro Z : " + str(gyro_data['z']))
            # print()
            # print("-------------------------------")
            # time.sleep(1)

    """def read_ir_sensor(self):
        if GPIO.input(self.ir_gpio):
            # If no object is near
            # GPIO.output(led_pin, False)
            self.presence = True
            while GPIO.input(self.ir_gpio):
                time.sleep(0.2)
        else:
            # If an object is detected
            # GPIO.output(led_pin, True)
            self.presence = False

        return f' ir_sensor = {self.presence}'"""

    def read_thermometer(self):
        self.object_temperature = self.thermometer.get_object_1()
        self.ambient_temperature = self.thermometer.get_ambient()

        #print(f'object temperature = {self.object_temperature} \n ambient temperature = {self.ambient_temperature}')


    def read_speedometer(self):
        if GPIO.event_detected(self.rpm_gpio):
            self.counted_motor_slots += 1
            #print(f'Slots counted = {self.counted_motor_slots}')
        if self.counted_motor_slots == self.motor_slots:
            while True:
                # Measure the time between the 40 blades
                elapsed_time = time.time() - self.start_time_rpm_reading

                # Calculate the RPM
                self.rpm_value = 1 / elapsed_time * 60

                # reinitialize variables
                self.counted_motor_slots = 0
                self.start_time_rpm_reading = time.time()

                print(f'velocity = {self.rpm_value}')
                
                break
    
    def read_microphone(self):
        if self.arduino_connection.in_waiting > 0:
            arduino_data = self.arduino_connection.readline()
            try:
                self.audio_value = str(arduino_data[0:len(arduino_data)].decode('utf-8')).rstrip()
            except ValueError:
                raise InputError('got bad value {}'.format(decoded_values))
            
            print(self.audio_value)
    
        #return decoded_values


    def get_all_readings(self):
        self.read_speedometer()
        #self.read_accelerometer()
        self.read_thermometer()
        #self.read_microphone()
    
    def stop_and_clean_reading(self):
        GPIO.cleanup()
        self.arduino_connection.close()

class MotorControl:
    
    # declare global variable for class
    global motor_pwm
    motor_pwm = None
    
    def __init__(self, velocity):
        self.control_velocity = velocity
        self.motor_pwm = motor_pwm
        
        

    def gpio_setup(self):
        # set gpio configuration to use default gpio board configuration
        GPIO.setmode(GPIO.BCM)
        
        # define dute_cycle gpio
        control_pin = 13
        
        # set duty_cycle_gpio as output and pwm mode
        GPIO.setup(control_pin, GPIO.OUT)
        self.motor_pwm = GPIO.PWM(control_pin, 500)
        
        self.motor_pwm.start(0)

    
    def stop_motor(self):
        self.motor_pwm.ChangeDutyCycle(self.control_velocity)
        
    def start_motor(self):
        self.motor_pwm.ChangeDutyCycle(self.control_velocity)
        
    def control_velocity(self):
        while True:
            duty = int(input('Entre com o Ciclo de Trabalho -> 0 a 100: '))
            print('Valor deve estar entre 0 e 100')
            self.motor_pwm.ChangeDutyCycle(duty)

    def turnOff_motor(self):
        self.motor_pwm.ChangeDutyCycle(0)
    
    