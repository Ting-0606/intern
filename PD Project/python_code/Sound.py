import time
import RPi.GPIO as GPIO
import threading

class Sound:
    # Musical notes frequencies: [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
    _notes = [262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 492, 523]
    DEFAULT_SOUND_DELAY = 50  # Default duration of one beat in ms

    def __init__(self, buzpin=23 , delta=DEFAULT_SOUND_DELAY):#buzpin = GPIO23
        """Initialize with physical buzzer pin"""
        self._buzpin = buzpin
        self._delta = delta
        self._enable = False
        
        GPIO.setmode(GPIO.BCM) #It tells the RPi.GPIO library to use the Broadcom chip's native pin numbers (also called "BCM" or "GPIO" numbers)
        GPIO.setup(self._buzpin, GPIO.OUT)
        self._pwm = None

    def set_enable(self, val):
        """Turn ON or OFF buzzer sound feedback"""
        self._enable = val

    def get_enable(self):
        """Turn ON or OFF buzzer sound feedback"""
        return self._enable

    def play(self, melody, beat, n, enable_output):
        """Play melody tone beat-by-beat"""
    
        if not enable_output:#if sound disabled then exit
            return

        def play_thread():
            for i in range(n):
                if melody[i] > 0 :
                    freq = self._notes[melody[i]] # Get frequency from note table
                    self._pwm = GPIO.PWM(self._buzpin, freq)
                    self._pwm.start(50)
                    time.sleep(self._delta * beat[i] / 1000.0)#millisecond
                    self._pwm.stop()
                else:
                    # Rest/pause
                    time.sleep(self._delta * beat[i] / 1000.0)
                
                # Add delay between notes if needed
                if n > 1 and i < n-1:
                    time.sleep(self._delta * beat[i] / 1000.0)

        # Run in a thread to avoid blocking
        thread = threading.Thread(target=play_thread)
        thread.start()

   
       

    def welcome(self):
        """Play C-Major melody at startup: C -> E -> G -> C'"""
        melody = [1, 0, 4, 0, 7, 0, 12]  # C4, pause, E4, pause, G4, pause, C5
        beat = [2, 1, 2, 1, 2, 1, 2]
        self.play(melody, beat, 7, True)

    def alert(self, freq, n, forced=False):
        """Beep sound repeated N times"""
        melody = []
        beat = []
        enable_output = forced if forced else self._enable
        
        for i in range(n):
            melody.extend([freq, 0])  # note and pause
            beat.extend([1, 1])      # durations
        
        self.play(melody, beat, n*2, enable_output)

    def beep(self, freq, forced=True):
        """Beep sound once"""
        melody = [freq]
        beat = [1]
        enable_output = forced if forced else self._enable
        self.play(melody, beat, 1, enable_output)

    def mode(self, state):
        """Two beep sounds indicating WALK MODE"""
        melody = [5, 0, state * 5]  # F4, pause, mode-dependent note
        beat = [2, 1, 2]
        self.play(melody, beat, 3, True)

     def cleanup(self):
        """Clean up GPIO resources"""
        if self._pwm is not None:
            self._pwm.stop()
        GPIO.cleanup([self._buzpin])