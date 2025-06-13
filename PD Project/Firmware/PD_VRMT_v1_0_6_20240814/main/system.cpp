#include <Arduino.h>
#include "system.h"
#include <avr/wdt.h>

System::System() {};

void System::init(int pin_batt, int pin_charge, int pin_charge_led, int pin_power_supply) {
    _pin_batt = pin_batt;
    _pin_charge = pin_charge;
    _pin_charge_led = pin_charge_led;
    _pin_power_supply = pin_power_supply;
    pinMode(_pin_charge_led, OUTPUT);
    pinMode(_pin_power_supply, OUTPUT);

    digitalWrite(_pin_power_supply, HIGH);
}

void System::check_battery() {
    _voltage = analogRead(_pin_batt) * BATTERY_ADC;

    _charging = analogRead(_pin_charge);
    bool currently_is_charging = (_charging >= 200);
    if (currently_is_charging != _is_charging) {
        digitalWrite(_pin_charge_led, (currently_is_charging) ? HIGH : LOW);
        _is_charging = currently_is_charging;
    }
}

bool System::check_time(unsigned long* timer, unsigned long period) {
    // update the time passed since the last timer check
    // notify if a particular time period has passed
    _dt = micros() - *timer;
    if (_dt >= period) {
        // update the timer at the timed interval
        *timer = micros();
        return true;
    }
    return false;
}

float System::get_voltage() {
    return _voltage;
}

float System::get_charging() {
    return _charging;
}
