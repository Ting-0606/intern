import time
import RPi.GPIO as GPIO
import threading
#adsfjajflsadkf
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
        self._pwm = GPIO.PWM(self._buzpin, 440)  # Initialize PWM (dummy frequency)
        self._pwm.start(0)  # Start with 0% duty cycle (silent)

    def set_enable(self, val):
        """Turn ON or OFF buzzer sound feedback"""
        self._enable = val

    def get_enable(self):
        """Turn ON or OFF buzzer sound feedback"""
        return self._enable


     def _play_note(self, note_index, duration_ms):
        if note_index >= 0:  # Valid note
            self._pwm.ChangeFrequency(self._notes[note_index])
            self._pwm.ChangeDutyCycle(50)  # 50% volume
        time.sleep(duration_ms / 1000.0)#seconds
        self._pwm.ChangeDutyCycle(0)  # Silence after note/rest

    def play(self, melody, beat, n, enable_output):
        """Play melody tone beat-by-beat"""
    
        if not (enable_output or self._enable):
            return

        def play_thread():
            """Thread worker for playback."""
            try:
                for i in range(n):
                    self._play_note(melody[i], self._delta * beat[i])
                    # Add pause between notes (except last one)
                    if i < n - 1:
                        time.sleep(self._delta * beat[i] / 1000.0)
            finally:
                self._pwm.ChangeDutyCycle(0)  # Ensure silence on exit

        # Run in a thread to avoid blocking main program function
        threading.Thread(target=play_thread, daemon=True).start()#daemon threads are killed when main program exit
        

   
       

    def welcome(self):
        """Play C-Major melody at startup: C -> E -> G -> C'"""
        melody = [0, -1, 4, -1, 7, -1, 12]  # C4, pause, E4, pause, G4, pause, C5
        beat = [2, 1, 2, 1, 2, 1, 2]
        self.play(melody, beat, 7, True)

    def alert(self, freq, n, forced=False):
        """Beep sound repeated N times"""
        melody = []
        beat = []
        for _ in range(n):
            melody.extend([freq, -1])  # Note and rest
            beat.extend([1, 1])
        self.play(melody, beat, n*2, forced or self._enable)

    def beep(self, freq, forced=True):
        """Beep sound once"""
        self.play([freq], [1], 1, forced or self._enable)

    def mode(self, state):
        """Two beep sounds indicating WALK MODE"""
        melody = [5, -1, state * 5]  # F4, pause, mode-dependent note
        beat = [2, 1, 2]
        self.play(melody, beat, 3, True)

    def cleanup(self):
        """Clean up GPIO resources."""
        self._pwm.stop()
        GPIO.cleanup([self._buzpin])