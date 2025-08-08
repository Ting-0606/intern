import RPi.GPIO as GPIO
import time

LED_PIN = 25


GPIO.setmode(GPIO.BCM)  # Use BCM numbering (GPIO 25, not physical pin 22)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)   # LED OFF
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()