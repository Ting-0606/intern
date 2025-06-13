#ifndef __A4950__H__
#define __A4950__H__

#include "setup.h"

class A4950 {
    private:
        int _pin_a4950_in0;
        int _pin_a4950_in1;
        int _pin_a4950_led;
        int _pin_sw_0;
        int _pin_sw_1;

        bool _is_ready = false;
        bool _is_moving = false;
        int _is_pressed_sw_0 = 0;
        int _is_pressed_sw_1 = 0;
        
        void _motor_up();
        void _motor_down();
        void _motor_stop();
        void _update();

    public:
        enum State {
            DOWN = -1,
            STOP = 0,
            UP = 1
        } state = STOP;

        A4950();
        void init(int pin_M0, int pin_M1, int pin_M_LED, int pin_sw_0, int pin_sw_1);
        void set_ready(bool val);
        void set_state(int val);
        void check_switch();
        bool get_is_moving();
};

#endif
