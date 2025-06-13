#ifndef __SETUP__H__
#define __SETUP__H__

//      PB5,   D13 |       |  D12,PB4, CIP0
//            +3V3 |       | ~D11,PB3, COPI
//            AREF |       | ~D10,PB2
// ADC0,PC0,A0,D14 |       | ~D9 ,PB1
// ADC1,PC1,A1,D15 |       |  D8 ,PB0
// ADC2,PC2,A2,D16 |       |  D7 ,PD7
// ADC3,PC3,A3,D17 |       | ~D6 ,PD6
// ADC4,PC4,A4,D18 |       | ~D5 ,PD5
// ADC5,PC5,A5,D19 |       |  D4 ,PD4
// ADC6,    A6     |       | ~D3 ,PD3
// ADC7,    A7     |       |  D2 ,PD2
//             +5V |       | GND
//      PC6,   RST |       | RST, PC6
//             GND |       | D0/RX, PD0
//             VIN |       | D1/TX, PD1

#define VERSION                 "V1.0.2"
#define BAUDRATE                115200
#define LOOP_TIME               50000       // loop at 20 Hz
#define ONE_SEC                 1000000     // loop at 1 Hz

// HX711 Load Cells
#define HX711_PD_SCK_DRAIN      2       // PD2
#define HX711_DOUT_DRAIN        3       // PD3
#define HX711_PD_SCK_FILL       4       // PD4
#define HX711_DOUT_FILL         5       // PD5

// A4950
#define A4950_IN0               6       // PD6
#define A4950_LED               8       // PB0
#define A4950_IN1               9       // PB1
#define MOTOR_SWITCH_0          17      // PC3
#define MOTOR_SWITCH_1          16      // PC2

// BLE
#define BLE_CONNECT             7       // PD7
#define BLE_HEADER              0xFF
#define BLE_HEADER_LEN          4
#define BLE_RX_DATA_LEN         50
#define BLE_TX_DATA_LEN         18

// OTHER DEVICES
#define PIN_LED                 10      // PB2
#define PIN_CAM                 18      // PC4
#define PIN_BUZZ                19      // PC5
#define PIN_CHARGING            13      // PB5
#define PIN_CHARGE_ADC          A0
#define PIN_BATTERY             A1
#define PIN_OUT_LED             A6

#endif
