// Ankle Robot Control Program for Arduino Nano
//
// Sound Tone Generator
// Copyright reserved (Jan 2022)


#include <Arduino.h>
#include "Sound.h"


Sound::Sound() {};
Sound::Sound(int pin) {
    _buzpin = pin;
    pinMode(_buzpin, OUTPUT);
}
Sound::Sound(int pin, int d) {
    _buzpin = pin;
    _delta = d;
    pinMode(_buzpin, OUTPUT);
}

void Sound::set_enable(bool val) {
    // Turn ON or OFF buzzer sound feedback
    _enable = val;
}

bool Sound::get_enable() {
    // Turn ON or OFF buzzer sound feedback
    return _enable;
}

void Sound::play(int *melody, int *beat, int n, bool enable_output) {
    if (enable_output) {
        // Play melody tone beat-by-beat
        for (int i = 0; i < n; i++) {
            if (melody[i]) {
                // produce music tone at specified frequency
                tone(_buzpin, melody[i], _delta * beat[i]);
            }
            if (n > 1) {
                // Add delay in between multiple beats
                delay(_delta * beat[i]);
            }
        }
    }
}

void Sound::welcome() {
    // Play C-Major melody at startup: C -> E -> G -> C'
    // [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
    int melody[7] = {_notes[0], 0, _notes[4], 0, _notes[7], 0, _notes[12]};
    int beat[7] = {2, 1, 2, 1, 2, 1, 2};
    play(melody, beat, 7, true);
}

void Sound::alert(int freq, int n, bool forced) {
    // Beep sound repeated N times
    // [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
    int melody[n * 2];
    int beat[n * 2];
    bool enable_output = (forced) ? true : _enable;
    for (int i = 0; i < n; i++) {
        // construct a sound beat packet with alternated beeps and pauses
        melody[i * 2] = _notes[freq];
        melody[i * 2 + 1] = 0;
        beat[i * 2] = 1;
        beat[i * 2 + 1] = 1;
    }
    play(melody, beat, n * 2, enable_output);
}

void Sound::beep(int freq) {
    // default beep is forced to enable
    beep(freq, true);
}

void Sound::beep(int freq, bool forced) {
    // Beep sound only ONCE in the BACKGROUND
    // If not forced, the beep enable/disable could be controlled
    // [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
    int melody[1] = {_notes[freq]};
    int beat[1] = {1};
    // enable/disable sound feedback output
    bool enable_output = (forced) ? true : _enable;
    play(melody, beat, 1, enable_output);
}

void Sound::mode(int state) {
    // Two beep sounds with three patterns indicating WALK MODE
    // [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
    int melody[3] = {_notes[5], 0, _notes[state * 5]};
    int beat[3] = {2, 1, 2};
    play(melody, beat, 3, true);
}
