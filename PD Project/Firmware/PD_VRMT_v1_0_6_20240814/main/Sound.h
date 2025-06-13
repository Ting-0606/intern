#ifndef __SOUND_H__
#define __SOUND_H__

// Sound frequency : [C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4, C5]
#define MUSICAL_NOTES {262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 492, 523}
#define DEFAULT_SOUND_DELAY     50  // Default duration of one beat


class Sound {
    private:
        int _buzpin;
        int _delta = DEFAULT_SOUND_DELAY;
        const int _notes[13] = MUSICAL_NOTES;
        bool _enable = false;
        
    public:
        Sound();
        Sound(int pin);
        Sound(int pin, int d);
        
        bool get_enable();
        void set_enable(bool val);
        
        void play(int* melody, int* beat, int n, bool enable_output);
        void welcome();
        void alert(int freq, int n, bool forced);
        void beep(int freq);
        void beep(int freq, bool forced);
        void mode(int state);
};

#endif /* _SOUND_ */
