#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.cleanup()  # Clean up previous configurations

CHECK_PIN = 25  # GPIO 25 (BCM numbering)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHECK_PIN, GPIO.OUT)  # Set pin as INPUT

print(f"Monitoring GPIO {CHECK_PIN}. Press Ctrl+C to stop.")
try:
    while True:
        GPIO.output(CHECK_PIN, GPIO.HIGH)  # LED ON
        pin_state = GPIO.input(CHECK_PIN)
        time.sleep(0.01)
        print(f"GPIO {CHECK_PIN} is HIGH {pin_state}")
        time.sleep(1)

        GPIO.output(CHECK_PIN, GPIO.LOW)   # LED OFF
        pin_state_2 = GPIO.input(CHECK_PIN)
        time.sleep(0.01)
        print(f"GPIO {CHECK_PIN} is LOW {pin_state_2}")
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nScript stopped.")