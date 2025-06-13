#ifndef __CHECK__H__
#define __CHECK__H__

#define BATTERY_ADC             0.01807

class System {
    private:
        int _pin_batt;
        int _pin_charge;
        int _pin_charge_led;
        int _pin_power_supply;

        bool _is_charging;
        float _dt;
        float _voltage;
        float _charging;

    public:
        System();

        void init(int pin_batt, int pin_charge, int pin_charge_led, int pin_power_supply);
        void check_battery();
        bool check_time(unsigned long* timer, unsigned long period);
        float get_voltage();
        float get_charging();
};

#endif
