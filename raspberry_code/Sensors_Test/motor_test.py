import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

control_pin = 13

GPIO.setup(control_pin, GPIO.OUT)
motor_pwm = GPIO.PWM(control_pin, 500)
motor_pwm.start(0)
duty = 0

try:
    while True:
            duty = int(input('Entre com o Ciclo de Trabalho -> 0 a 100: '))
            print('Valor deve estar entre 0 e 100')
            motor_pwm.ChangeDutyCycle(duty)
            print(duty)
finally:
    print('Limpando...')
    GPIO.cleanup()
