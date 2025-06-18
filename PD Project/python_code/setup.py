# setup.py - Raspberry Pi Pin Configuration

# System Configuration
VERSION = "V1.0.2"
BAUDRATE = 115200
LOOP_TIME = 50000        # loop at 20 Hz (in microseconds)
ONE_SEC = 1000000        # loop at 1 Hz (in microseconds)

# HX711 Load Cells 
HX711_PD_SCK_DRAIN = 2   # GPIO2 (Physical Pin 3)
HX711_DOUT_DRAIN = 3     # GPIO3 (Physical Pin 5)
HX711_PD_SCK_FILL = 4    # GPIO4 (Physical Pin 7)
HX711_DOUT_FILL = 5      # GPIO5 (Physical Pin 29)

# A4950 Motor Driver
A4950_IN0 = 6            # GPIO6 (Physical Pin 31)
A4950_LED = 8            # GPIO8 (Physical Pin 24)
A4950_IN1 = 9            # GPIO9 (Physical Pin 21)
MOTOR_SWITCH_0 = 17      # GPIO17 (Physical Pin 11)
MOTOR_SWITCH_1 = 16      # GPIO16 (Physical Pin 36)

# Bluetooth (BLE)
BLE_CONNECT = 7          # GPIO7 (Physical Pin 26)
BLE_HEADER = 0xFF
BLE_HEADER_LEN = 4
BLE_RX_DATA_LEN = 50
BLE_TX_DATA_LEN = 18

# Other Devices
PIN_LED = 10             # GPIO10 (Physical Pin 19)
PIN_CAM = 18             # GPIO18 (Physical Pin 12)
PIN_BUZZ = 19            # GPIO19 (Physical Pin 35)
PIN_CHARGING = 13        # GPIO13 (Physical Pin 33)
PIN_CHARGE_ADC = 0       # ADC Channel 0
PIN_BATTERY = 1          # ADC Channel 1
PIN_OUT_LED = 6          # Using ADC Channel 6 (if available)

# ADC Configuration 
ADC_VREF = 3.3           # Reference voltage
ADC_MAX_VALUE = 1023     # 10-bit ADC resolution

