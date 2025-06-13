#ifndef __UART__H__
#define __UART__H__

#include "setup.h"
#include "HX711.h"
#include "A4950.h"
#include "system.h"
#include "memory.h"
#include "Sound.h"

typedef union {
    // Easy convert between one 4-byte double and four bytes
    double floatpt;
    byte binary[4];
} binaryFloat;

class UART {
    private:
        binaryFloat _buffered;
        byte _buffer_hd[BLE_HEADER_LEN];
        byte _buffer_data[BLE_RX_DATA_LEN];
        byte _idx;
        int _cmd;
        int _len;
        int _chksum_rx;
        int _chksum_tx;
        bool _is_streaming = false;
        bool _is_connected = true;  // true to trigger the reset at reboot
        
        HX711* _ptr_weight_drain;
        HX711* _ptr_weight_fill;
        A4950* _ptr_motor;
        System* _ptr_sys;
        Memory* _ptr_mem;
        Sound* _ptr_buz;

    public:
        UART(HX711* weight_fill, HX711* weight_drain, A4950* motor, System* sys, Memory* mem, Sound* buz);
        void init(int baud);
        void check_connection(int pin_connect);
        void data_buffering(byte val);
        void data_buffering(float val);
        void data_send();
        void data_receive();
        void buffer_shift(byte buffer[BLE_HEADER_LEN]);
};

#endif
