import RPi.GPIO as GPIO
from enum import Enum

class A4950:
    class State(Enum):
        DOWN = -1
        STOP = 0
        UP = 1

    def __init__(self):
        self._pin_a4950_in0 = None
        self._pin_a4950_in1 = None
        self._pin_a4950_led = None
        self._pin_sw_0 = None
        self._pin_sw_1 = None
        
        self._is_ready = False
        self._is_moving = False
        self._is_pressed_sw_0 = 0
        self._is_pressed_sw_1 = 0
        self.state = self.State.STOP

    def init(self, pin_M0 = , pin_M1 = , pin_M_LED = , pin_sw_0 = , pin_sw_1 = ):
        self._pin_a4950_in0 = pin_M0
        self._pin_a4950_in1 = pin_M1
        self._pin_a4950_led = pin_M_LED
        self._pin_sw_0 = pin_sw_0
        self._pin_sw_1 = pin_sw_1
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_a4950_in0, GPIO.OUT)
        GPIO.setup(self._pin_a4950_in1, GPIO.OUT)
        GPIO.setup(self._pin_a4950_led, GPIO.OUT)
        GPIO.setup(self._pin_sw_0, GPIO.IN, pull_up=GPIO.PUD_UP)# high when not pressed
        GPIO.setup(self._pin_sw_1, GPIO.IN, pull_up=GPIO.PUD_UP)
        


       
        self._motor_stop()

    def set_ready(self, val):
        self._is_ready = val

    def set_state(self, val):
        self.state = self.State(val)
        self._update()

    def check_switch(self):
        current_state_sw_0 = GPIO.input(self._pin_sw_0)# low when pressed
        current_state_sw_1 = GPIO.input(self._pin_sw_1)
        
        if ((self._is_pressed_sw_0 != current_state_sw_0) or #check press action
            (self._is_pressed_sw_1 != current_state_sw_1)):
            
            if current_state_sw_0 > current_state_sw_1: # 1>0 , sw_1 should be pressed
                self.set_state(self.State.UP.value)
            elif current_state_sw_0 < current_state_sw_1:# 0<1, sw_0 should be pressed
                self.set_state(self.State.DOWN.value)
            else:
                self.set_state(self.State.STOP.value) # 1=1, no one pressed
                
            #update the current state
            self._is_pressed_sw_0 = current_state_sw_0 
            self._is_pressed_sw_1 = current_state_sw_1

    def _update(self):
        if self._is_ready:
            if self.state == self.State.DOWN:
                self._motor_down()
            elif self.state == self.State.STOP:
                self._motor_stop()
            elif self.state == self.State.UP:
                self._motor_up()

    def _motor_up(self):
        GPIO.output(self._pin_a4950_in0, GPIO.HIGH)
        GPIO.output(self._pin_a4950_in1, GPIO.LOW)
        GPIO.output(self._pin_a4950_led, GPIO.HIGH)
        self._is_moving = True

    def _motor_down(self):
        GPIO.output(self._pin_a4950_in0, GPIO.LOW)
        GPIO.output(self._pin_a4950_in1, GPIO.HIGH)
        GPIO.output(self._pin_a4950_led, GPIO.HIGH)
        self._is_moving = True

    def _motor_stop(self):
        GPIO.output(self._pin_a4950_in0, GPIO.LOW)
        GPIO.output(self._pin_a4950_in1, GPIO.LOW)
        GPIO.output(self._pin_a4950_led, GPIO.LOW)
        self._is_moving = False

    def get_is_moving(self):
        return self._is_moving

    def cleanup(self):
        self._motor_stop()
        GPIO.cleanup()