import RPi.GPIO as GPIO
import time

GPIO.cleanup()
SW_0 = 5 #Forward M
SW_1 = 6 #Reverse M

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


try:
    while True:
        print(f"SW_0 state(F/GPIO5): {'HIGH (unpressed)' if GPIO.input(SW_0) else 'LOW (pressed)'} | SW_1 state(R/GPIO6): {'HIGH (unpressed)' if GPIO.input(SW_1) else 'LOW (pressed)'}")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()