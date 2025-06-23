import RPi.GPIO as GPIO
import time

class HX711:
    def __init__(self, pin_dout_fill=17, pin_pd_sck_fill=16, pin_dout_drain=27, pin_pd_sck_drain=26):
        # Fill load cell pins
        self._pin_dout_fill = pin_dout_fill
        self._pin_pd_sck_fill = pin_pd_sck_fill
        
        # Drain load cell pins
        self._pin_dout_drain = pin_dout_drain
        self._pin_pd_sck_drain = pin_pd_sck_drain
        
        # Calibration values for each cell
        self._zero_fill = 9000000.0   # Default tare for fill cell
        self._cal_fill = 870.0        # Default cal factor for fill cell
        self._zero_drain = 9000000.0  # Default tare for drain cell
        self._cal_drain = 870.0       # Default cal factor for drain cell
        
        GPIO.setmode(GPIO.BCM)
        
        # Setup fill cell pins
        GPIO.setup(self._pin_dout_fill, GPIO.IN)
        GPIO.setup(self._pin_pd_sck_fill, GPIO.OUT)
        GPIO.output(self._pin_pd_sck_fill, GPIO.LOW)
        
        # Setup drain cell pins
        GPIO.setup(self._pin_dout_drain, GPIO.IN)
        GPIO.setup(self._pin_pd_sck_drain, GPIO.OUT)
        GPIO.output(self._pin_pd_sck_drain, GPIO.LOW)



    def _read_single(self, dout_pin, sck_pin):
        """Internal method to read from a single HX711"""
        count = 0
        
        while GPIO.input(dout_pin) == GPIO.HIGH:
            time.sleep(0.001)
        
        for i in range(24):
            GPIO.output(sck_pin, GPIO.HIGH)
            time.sleep(0.000001)
            count = count << 1
            GPIO.output(sck_pin, GPIO.LOW)
            time.sleep(0.000001)
            
            if GPIO.input(dout_pin) == GPIO.HIGH:
                count += 1
        
        # 25th pulse to set next conversion
        GPIO.output(sck_pin, GPIO.HIGH)
        time.sleep(0.000001)
        GPIO.output(sck_pin, GPIO.LOW)
        time.sleep(0.000001)
        
        count ^= 0x800000
        return count

    # Read methods for each cell
    def read_fill(self):
        return self._read_single(self._pin_dout_fill, self._pin_pd_sck_fill)
    
    def read_drain(self):
        return self._read_single(self._pin_dout_drain, self._pin_pd_sck_drain)
    
    # Calibration methods for fill cell
    def set_zero_fill(self): #read ADC data when no weight
        self._zero_fill = self.read_fill()
        return self._zero_fill

    def set_cal_fill(self, known_weight=1000.0): #read ADC data when weight 1000g
        reading = self.read_fill()
        self._cal_fill = (reading - self._zero_fill) / known_weight
        return self._cal_fill

    # Calibration methods for drain cell
    def set_zero_drain(self):
        self._zero_drain = self.read_drain()
        return self._zero_drain

    def set_cal_drain(self, known_weight=1000.0):
        reading = self.read_drain()
        self._cal_drain = (reading - self._zero_drain) / known_weight
        return self._cal_drain

    # Weight calculation methods
    def get_weight_fill(self):
        return (self.read_fill() - self._zero_fill) / self._cal_fill
    
    def get_weight_drain(self):
        return (self.read_drain() - self._zero_drain) / self._cal_drain

    # Getter methods for calibration values
    def get_zero_fill(self):
        return self._zero_fill

    def get_cal_fill(self):
        return self._cal_fill

    def get_zero_drain(self):
        return self._zero_drain

    def get_cal_drain(self):
        return self._cal_drain

    # Input methods for manual calibration
    def input_zero_fill(self, val):
        self._zero_fill = val

    def input_cal_fill(self, val):
        self._cal_fill = val

    def input_zero_drain(self, val):
        self._zero_drain = val

    def input_cal_drain(self, val):
        self._cal_drain = val

    def cleanup(self):
        GPIO.cleanup()
