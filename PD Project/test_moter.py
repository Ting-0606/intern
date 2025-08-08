import RPi.GPIO as GPIO
import time

GPIO.cleanup()
IN1 = 5 #Forward M
IN2 = 6 #Reverse M

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.output(IN1,GPIO.HIGH)#adjust high low alternatively
GPIO.output(IN2,GPIO.LOW)

try:
    while True:
        print(f"{GPIO.input(IN1)} | {GPIO.input(IN2) }")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()