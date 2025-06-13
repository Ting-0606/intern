#include <Arduino.h>
#include "setup.h"
#include "A4950.h"

A4950::A4950() {};

void A4950::init(int pin_M0, int pin_M1, int pin_M_LED, int pin_sw_0, int pin_sw_1) {
    _pin_a4950_in0 = pin_M0;
    _pin_a4950_in1 = pin_M1;
    _pin_a4950_led = pin_M_LED;
    _pin_sw_0 = pin_sw_0;
    _pin_sw_1 = pin_sw_1;
    pinMode(_pin_a4950_in0, OUTPUT);
    pinMode(_pin_a4950_in1, OUTPUT);
    pinMode(_pin_a4950_led, OUTPUT);
    pinMode(_pin_sw_0, INPUT_PULLUP);
    pinMode(_pin_sw_1, INPUT_PULLUP);
}

void A4950::set_ready(bool val) {
    _is_ready = val;
}

void A4950::set_state(int val) {
    state = val;
    _update();
}

void A4950::check_switch() {
    int current_state_sw_0 = digitalRead(_pin_sw_0);
    int current_state_sw_1 = digitalRead(_pin_sw_1);
    if ((_is_pressed_sw_0 != current_state_sw_0) || (_is_pressed_sw_1 != current_state_sw_1)) {
        if (current_state_sw_0 > current_state_sw_1) {
            set_state(UP);
        }
        if (current_state_sw_0 < current_state_sw_1) {
            set_state(DOWN);
        }
        if (current_state_sw_0 == current_state_sw_1) {
            set_state(STOP);
        }
        _is_pressed_sw_0 = current_state_sw_0;
        _is_pressed_sw_1 = current_state_sw_1;
    }
}

void A4950::_update() {
    if (_is_ready) {
        switch (state) {
            case DOWN:
                _motor_down();
                break;
            case STOP:
                _motor_stop();
                break;
            case UP:
                _motor_up();
                break;
            default:
                break;
        }
    }
}

void A4950::_motor_up(){
    digitalWrite(_pin_a4950_in0, HIGH);
    digitalWrite(_pin_a4950_in1, LOW);
    digitalWrite(_pin_a4950_led, HIGH);
    _is_moving = true;
}

void A4950::_motor_down(){
    digitalWrite(_pin_a4950_in0, LOW);
    digitalWrite(_pin_a4950_in1, HIGH);
    digitalWrite(_pin_a4950_led, HIGH);
    _is_moving = true;
}

void A4950::_motor_stop(){
    digitalWrite(_pin_a4950_in0, LOW);
    digitalWrite(_pin_a4950_in1, LOW);
    digitalWrite(_pin_a4950_led, LOW);
    _is_moving = false;
}

bool A4950::get_is_moving() {
    return _is_moving;
}
