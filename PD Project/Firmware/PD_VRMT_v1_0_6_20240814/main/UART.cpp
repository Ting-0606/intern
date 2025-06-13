#include <Arduino.h>
#include "setup.h"
#include "UART.h"

void(* resetFunc) (void) = 0; //declare reset function at address 0

UART::UART(HX711* weight_fill, HX711* weight_drain, A4950* motor, System* sys, Memory* mem, Sound* buz) {
    _ptr_weight_fill = weight_fill;
    _ptr_weight_drain = weight_drain;
    _ptr_motor = motor;
    _ptr_sys = sys;
    _ptr_mem = mem;
    _ptr_buz = buz;
}

void UART::init(int baud) {
    Serial.begin(BAUDRATE);
    Serial.println("Begin...");
    delay(1000);
    pinMode(PIN_LED, OUTPUT);
}

void UART::check_connection(int pin_connect) {
    bool currently_connected = digitalRead(pin_connect);
    if (currently_connected != _is_connected) {
        if (!currently_connected) {
            // when bluetooth connection lost...
            _is_streaming = false;
            _ptr_motor->set_state(_ptr_motor->STOP);
            digitalWrite(PIN_LED, LOW);
        }
    }
    _is_connected = currently_connected;
}

void UART::data_buffering(byte val) {
    _chksum_tx += val;
    Serial.write(byte(val));
}

void UART::data_buffering(float val) {
    _buffered.floatpt = val;
    for (int i = 0; i < 4; i++) {
        data_buffering(_buffered.binary[i]);
    }
}

void UART::data_send() {
    if (_is_streaming) {
        data_buffering(byte(BLE_HEADER));
        data_buffering(byte(BLE_HEADER));

        _chksum_tx = 0;
        data_buffering(byte(BLE_TX_DATA_LEN));
        data_buffering(byte(_idx));
        data_buffering(_ptr_weight_fill->get_weight());
        data_buffering(_ptr_weight_drain->get_weight());
        data_buffering(_ptr_sys->get_voltage());
        data_buffering(_ptr_sys->get_charging());
        data_buffering(byte(~_chksum_tx));
        
        _idx = (_idx < 99)? _idx + 1 : 0;
    }
}

void UART::data_receive() {
    if (Serial.available()) {
        // read and check header segment
        buffer_shift(_buffer_hd);
        Serial.readBytes(_buffer_hd, 1);

        if ((_buffer_hd[3] == BLE_HEADER) && (_buffer_hd[2] == BLE_HEADER)) {
            _cmd = _buffer_hd[1];
            _len = _buffer_hd[0];
            _chksum_rx = _cmd + _len; 
            
            // compute the checksum
            Serial.readBytes(_buffer_data, _len);
            for (int i = 0; i < _len - 1; i++) {
                _chksum_rx += _buffer_data[i];
            }

            // validate the checksum
            if (_buffer_data[_len - 1] == byte(~_chksum_rx)) {

                // tasks to be done
                switch (_cmd) {

                    case 'R':       // system reset
                        resetFunc();
                        break;

                    case 'D':       // show system data
                        if (!_is_streaming) {
                            Serial.print("Version: "); Serial.println(VERSION);
                            Serial.print("Battery (V): "); Serial.println(_ptr_sys->get_voltage());
                            Serial.print("Charging: "); Serial.println(_ptr_sys->get_charging());
                            Serial.print("Load Cell Fill: "); Serial.print(_ptr_weight_fill->get_zero());
                            Serial.print(" / "); Serial.println(_ptr_weight_fill->get_cal());
                            Serial.print("Load Cell Drain: "); Serial.print(_ptr_weight_drain->get_zero());
                            Serial.print(" / "); Serial.println(_ptr_weight_drain->get_cal());
                        }
                        break;

                    case 'L':       // camera LED on
                        digitalWrite(PIN_LED, HIGH);
                        break;
                    case 'l':       // camera LED off
                        digitalWrite(PIN_LED, LOW);
                        break;

                    case 'S':       // stream start
                        _is_streaming = true;
                        _ptr_motor->set_ready(false);
                        break;
                    case 's':       // stream stop
                        _is_streaming = false;
                        _ptr_motor->set_ready(true);
                        break;

                    case 'Z':       // set zero for load cell 0
                        _ptr_weight_fill->set_zero();
                        _ptr_mem->save();
                        break;
                    case 'z':       // set zero for load cell 1
                        _ptr_weight_drain->set_zero();
                        _ptr_mem->save();
                        break;
                        
                    case 'C':       // calibrate 1kg weight for load cell 0
                        _ptr_weight_fill->set_cal();
                        _ptr_mem->save();
                        break;
                    case 'c':       // calibrate 1kg weight for load cell 1
                        _ptr_weight_drain->set_cal();
                        _ptr_mem->save();
                        break;

                    case 'M':       // motor going up
                        _ptr_motor->set_state(_ptr_motor->UP);
                        break;
                    case 'm':       // motor going down
                        _ptr_motor->set_state(_ptr_motor->DOWN);
                        break;
                    case 'x':       // motor stop
                        _ptr_motor->set_state(_ptr_motor->STOP);
                        break;

                    case 'T':
                        // test motor
                        digitalWrite(PIN_BUZZ, HIGH);
                        _ptr_motor->set_state(_ptr_motor->UP);
                        delay(1000);
                        _ptr_motor->set_state(_ptr_motor->DOWN);
                        delay(1000);
                        _ptr_motor->set_state(_ptr_motor->STOP);
                        digitalWrite(PIN_BUZZ, LOW);
                        break;

                    case 'A':
                        // alarm
                        tone(PIN_BUZZ, 330, 500);
                        break;

                    case 'P':
                        // play music
                        _ptr_buz->beep(5);
                        break;

                    default:
                        break;
                }

                // check if there are more unread messages
                data_receive();
                return true;
            }
        }
        return data_receive();
    }
    return false;
}

void UART::buffer_shift(byte buffer[BLE_HEADER_LEN]) {
    for (int i = BLE_HEADER_LEN - 1; i > 0; i--) {
        buffer[i] = buffer[i-1];
    }
}
