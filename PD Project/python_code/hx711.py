import RPi.GPIO as GPIO
import time

class HX711:
    def __init__(self, pin_dout, pin_pd_sck):
        self._pin_dout = pin_dout
        self._pin_pd_sck = pin_pd_sck
        self._zero = 9000000.0   # Default tare (zero) value
        self._cal = 870.0        # Default calibration factor
        self.weight = 0.0 
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_dout, GPIO.IN)
        GPIO.setup(self._pin_pd_sck, GPIO.OUT)
        GPIO.output(self._pin_pd_sck, GPIO.LOW)

    # Read data
    def read(self):
        count = 0 #initialize count to store 24-bits reading (all bits 0)
        
        while GPIO.input(self._pin_dout) == GPIO.HIGH: # Loop exit when DOUT low
            time.sleep(0.001)
        
        for i in range(24):#clock out 24 bits
            GPIO.output(self._pin_pd_sck, GPIO.HIGH) # when clock pulse high, read output
            time.sleep(0.000001)
            count = count << 1 #left-shift operation (new bit shifted into LSB)
            GPIO.output(self._pin_pd_sck, GPIO.LOW)
            time.sleep(0.000001)
            
            if GPIO.input(self._pin_dout) == GPIO.HIGH:
                count += 1 
        
        # After read 24 bits
        GPIO.output(self._pin_pd_sck, GPIO.HIGH)# 25th pulse starts 
        time.sleep(0.000001)
        GPIO.output(self._pin_pd_sck, GPIO.LOW) # 25th pulse starts 
        time.sleep(0.000001)
        
        count ^= 0x800000 # turns from 2's complement to offset binary(only positive value)
        return count

    # Calibration
    def set_zero(self):
        self._zero = self.read()
        return self._zero

    def get_zero(self):
            return self._zero

    def set_cal(self, known_weight=1000.0):
        reading = self.read()
        self._cal = (reading - self._zero) / known_weight
        return self._cal

    def get_cal(self):
            return self._cal 

    def input_zero(self, val):
            self._zero = val

    def input_cal(self, val):
            self._cal = val


    # Weight calculation
    def get_weight(self):
        self._weight = (self.read() - self._zero) / self._cal
        return self._weight


    def cleanup(self):
        GPIO.cleanup()
