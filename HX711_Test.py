#!/usr/bin/python3
import RPi.GPIO as GPIO
from hx711 import HX711
import time

GPIO.cleanup()
try:
    hx711 = HX711(
        dout_pin=17,
        pd_sck_pin=16,
        channel='A',
        gain=64
    )

    hx711_2 = HX711(
        dout_pin=27,
        pd_sck_pin=26,
        channel='A',
        gain=64
    )

    hx711.reset()  # Reset the HX711
    hx711_2.reset()  # Reset the HX711
    
    while True:

        reading = hx711._read()
        reading_2 = hx711_2._read()
        print(f"1:{reading}")
        print(f"2:{reading_2}")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nScript stopped.")
    

