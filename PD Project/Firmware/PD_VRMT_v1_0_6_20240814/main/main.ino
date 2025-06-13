#include <Arduino.h>
#include "setup.h"

#include "HX711.h"
#include "A4950.h"
#include "system.h"
#include "memory.h"
#include "UART.h"
#include "Sound.h"

Sound buzz(PIN_BUZZ);
HX711 weight_fill;
HX711 weight_drain;
A4950 motor;
System sys;
Memory mem(&weight_fill, &weight_drain);
UART ble(&weight_fill, &weight_drain, &motor, &sys, &mem, &buzz);

unsigned long timer1 = micros();
unsigned long timer2 = micros();
bool toggle = false;

void setup() {    
    ble.init(BAUDRATE);
    sys.init(PIN_BATTERY, PIN_CHARGE_ADC, PIN_CHARGING, PIN_CAM);
    weight_fill.init(HX711_DOUT_FILL, HX711_PD_SCK_FILL);
    weight_drain.init(HX711_DOUT_DRAIN, HX711_PD_SCK_DRAIN);
    mem.init();
    motor.init(A4950_IN0, A4950_IN1, A4950_LED, MOTOR_SWITCH_0, MOTOR_SWITCH_1);
    motor.set_ready(true);

    pinMode(BLE_CONNECT, INPUT_PULLUP);
}

void loop() {
    if (sys.check_time(&timer1, LOOP_TIME)) {
        ble.check_connection(BLE_CONNECT);
        sys.check_battery();
        ble.data_receive();
        motor.check_switch();
        ble.data_send();
    }

    if (sys.check_time(&timer2, ONE_SEC)) {
        toggle = (motor.get_is_moving()) ? !toggle : false;
        if (toggle) {
          buzz.beep(5);
        }
    }
}
