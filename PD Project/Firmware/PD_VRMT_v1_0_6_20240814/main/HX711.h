#ifndef __HX711__H__
#define __HX711__H__

#include "setup.h"

class HX711 {
    private:
        int _ch;                 // channel
        int _pin_dout;           // serial data output
        int _pin_pd_sck;         // power down control (high active) and serial clock input
        float _zero = 9000000;
        float _cal = 870;

    public:
        float weight;             // 0=Fill (TOP), 1=Drain (BOTTOM)

        HX711();
        void init(int dout, int pd_sck);
        unsigned long read();
        unsigned long set_zero();
        unsigned long get_zero();
        unsigned long set_cal();
        unsigned long get_cal();
        void input_zero(float val);
        void input_cal(float val);
        float get_weight();
};

#endif
