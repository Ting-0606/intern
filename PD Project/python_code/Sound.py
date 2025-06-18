import time
import pygame
import threading

class Sound:
    # Musical notes frequencies: [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
    _notes = [262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 492, 523]
    DEFAULT_SOUND_DELAY = 50  # Default duration of one beat in ms

    def __init__(self, pin=None, delta=DEFAULT_SOUND_DELAY):
        """Initialize sound system
        
        Note: On Raspberry Pi, the 'pin' parameter is ignored since we use pygame mixer
        instead of hardware PWM through a GPIO pin.
        """
        pygame.mixer.init()
        self._delta = delta
        self._enable = False
        self._current_sound = None

    def set_enable(self, val):
        """Turn ON or OFF buzzer sound feedback"""
        self._enable = val

    def get_enable(self):
        """Turn ON or OFF buzzer sound feedback"""
        return self._enable

    def play(self, melody, beat, n, enable_output):
        """Play melody tone beat-by-beat
        
        Args:
            melody: List of note indices (0-12) or 0 for silence
            beat: List of beat durations
            n: Number of notes to play
            enable_output: Whether to actually play the sound
        """
        if not enable_output:
            return

        def play_thread():
            for i in range(n):
                if melody[i] > 0 and melody[i] < len(self._notes):
                    # Generate tone using pygame
                    freq = self._notes[melody[i]]
                    # Create a square wave for the buzzer effect
                    sound = pygame.mixer.Sound(buffer=self._generate_beep(freq, self._delta * beat[i]))
                    sound.play()
                    self._current_sound = sound
                    time.sleep(self._delta * beat[i] / 1000.0)
                else:
                    # Rest/pause
                    time.sleep(self._delta * beat[i] / 1000.0)
                if n > 1 and i < n-1:
                    # Add delay between notes
                    time.sleep(self._delta * beat[i] / 1000.0)

        # Run in a thread to avoid blocking
        thread = threading.Thread(target=play_thread)
        thread.start()

    def _generate_beep(self, frequency, duration):# work as tone()
        """Generate a square wave beep sound"""
        sample_rate = 44100
        samples = int(sample_rate * duration / 1000.0)
        buf = numpy.zeros((samples, 2), dtype=numpy.int16)
        amplitude = 32767  # Max amplitude for 16-bit audio
        
        for s in range(samples):
            t = float(s) / sample_rate  # time in seconds
            # Square wave approximation
            val = amplitude if (t * frequency) % 1 < 0.5 else -amplitude
            buf[s][0] = val  # left channel
            buf[s][1] = val  # right channel
        
        return buf

    def welcome(self):
        """Play C-Major melody at startup: C -> E -> G -> C'"""
        melody = [0, 0, 4, 0, 7, 0, 12]  # C4, pause, E4, pause, G4, pause, C5
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
        """Clean up audio resources"""
        pygame.mixer.quit()