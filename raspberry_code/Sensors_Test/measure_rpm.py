"""import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# define pin for IR Sensor
IR_Sensor_Pin = 21

# set pin mode as input
GPIO.setup(IR_Sensor_Pin, GPIO.IN)

# define number of wheel slots
Wheel_Slots = 40

# initialize variable to store counted slots by IR Sensor
Counted_Slots = 0

# declare variable to store previous time
Previous_Time = 0

def get_time():
 	return time.time()
    
def count_slots(c):
    global Counted_Slots
    Counted_Slots+=1
    
    if Counted_Slots == 40:
        measure_rpm()


def measure_rpm():
    global Previous_Time
    global Counted_Slots
    
    time = get_time() - Previous_Time
    rpm = (Counted_Slots/time) * 60 * Wheel_Slots
    print(rpm)
    Previous_Time = get_time()
    Counted_Slots = 0
    
 # execute the get_rpm function when a HIGH signal is detected
GPIO.add_event_detect(IR_Sensor_Pin, GPIO.RISING, callback=count_slots)

try:
    while True: # create an infinte loop to keep the script running
        time.sleep(0.1)
except KeyboardInterrupt:
 	print ("  Quit")
 	GPIO.cleanup()"""

import RPi.GPIO as GPIO
import time

def aa():
    #set up GPIO BCM mode
    GPIO.setmode(GPIO.BCM)

    #set up GPIO pin
    GPIO_pin = 21

    #Set up GPIO pin as Input
    GPIO.setup(GPIO_pin, GPIO.IN)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(21, GPIO.FALLING, bouncetime=15)

    # Variables 
    rpm = 0 
    start_Time = time.time()
    slots = 0

    # Count number of blades 
    while True: 
        if GPIO.event_detected(21):
            slots+=1
        if slots == 40:
            while True:
                # Measure the time between the 40 blades 
                elapsedTime = time.time() - start_Time 

                # Calculate the RPM 
                rpm = 1/elapsedTime * 60

                # Print results 
                print("RPM:", rpm)
                slots = 0
                start_Time = time.time()
                break

    GPIO.cleanup()

if __name__ == '__main__':
    aa()
