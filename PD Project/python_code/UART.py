import serial
import struct
import time
import RPi.GPIO as GPIO
from setup import *  # Import all configuration constants

class UART:
    def __init__(self, weight_fill, weight_drain, motor, system, memory, buzzer):
        """Initialize with all required components"""
        self._weight_fill = weight_fill
        self._weight_drain = weight_drain
        self._motor = motor
        self._system = system
        self._memory = memory
        self._buzzer = buzzer
        
        self._buffered = bytearray(4)
        self._buffer_hd = bytearray(BLE_HEADER_LEN)
        self._buffer_data = bytearray(BLE_RX_DATA_LEN)
        self._idx = 0
        self._cmd = 0
        self._len = 0
        self._chksum_rx = 0
        self._chksum_tx = 0
        self._is_streaming = False
        self._is_connected = True
        self._serial = None
        
        # Initialize LED pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_LED, GPIO.OUT)
        GPIO.output(PIN_LED, GPIO.LOW)

    def init(self, baudrate=None, port='/dev/serial0'):
        """Initialize UART communication"""
        try:
            self._serial = serial.Serial(
                port=port,
                baudrate=baudrate if baudrate else BAUDRATE,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.1  # Short timeout for non-blocking reads
            )
            print(f"UART initialized at {baudrate if baudrate else BAUDRATE} baud")
            time.sleep(1)  # Allow time for connection
            
        except Exception as e:
            print(f"UART initialization failed: {e}")
            raise

    def check_connection(self, pin_connect=None):
        """Check Bluetooth connection status"""
        connect_pin = pin_connect if pin_connect else BLE_CONNECT
        currently_connected = GPIO.input(connect_pin)
        
        if currently_connected != self._is_connected:
            if not currently_connected:
                # Connection lost
                self._is_streaming = False
                self._motor.set_state(self._motor.State.STOP.value)
                GPIO.output(PIN_LED, GPIO.LOW)
                print("Bluetooth disconnected")
            else:
                print("Bluetooth connected")
                
            self._is_connected = currently_connected

    def data_buffering(self, val):
        """Buffer and send data with checksum calculation"""
        if isinstance(val, int):
            self._chksum_tx += val
            self._serial.write(bytes([val]))
        elif isinstance(val, float):
            # Pack float into 4 bytes
            packed = struct.pack('f', val)
            for byte in packed:
                self.data_buffering(byte)

    def data_send(self):
        """Send data packet if streaming is enabled"""
        if self._is_streaming and self._serial and self._serial.is_open:
            try:
                # Send packet header
                self.data_buffering(BLE_HEADER)
                self.data_buffering(BLE_HEADER)

                # Prepare data packet
                self._chksum_tx = 0
                self.data_buffering(BLE_TX_DATA_LEN)
                self.data_buffering(self._idx)
                self.data_buffering(self._weight_fill.get_weight())
                self.data_buffering(self._weight_drain.get_weight())
                self.data_buffering(self._system.get_voltage())
                self.data_buffering(self._system.get_charging())
                
                # Send checksum (one's complement)
                self.data_buffering(~self._chksum_tx & 0xFF)
                
                # Increment packet counter
                self._idx = (self._idx + 1) % 100

            except Exception as e:
                print(f"Data send error: {e}")

    def data_receive(self):
        """Receive and process incoming commands"""
        if self._serial and self._serial.in_waiting:
            try:
                # Shift buffer and read new byte
                self.buffer_shift(self._buffer_hd)
                self._buffer_hd[0] = self._serial.read(1)[0]

                # Check for valid header
                if (self._buffer_hd[3] == BLE_HEADER and 
                    self._buffer_hd[2] == BLE_HEADER):
                    
                    self._cmd = self._buffer_hd[1]
                    self._len = self._buffer_hd[0]
                    self._chksum_rx = self._cmd + self._len
                    
                    # Read data payload
                    self._buffer_data = self._serial.read(self._len)
                    
                    # Verify checksum
                    for i in range(self._len - 1):
                        self._chksum_rx += self._buffer_data[i]
                    
                    if self._buffer_data[self._len - 1] == (~self._chksum_rx & 0xFF):
                        return self._process_command()
                    
            except Exception as e:
                print(f"Data receive error: {e}")
                
        return False

    def _process_command(self):
        """Execute received command"""
        cmd_char = chr(self._cmd)
        
        if cmd_char == 'R':  # System reset
            print("Reset command received")
            # Implement system reset logic
            
        elif cmd_char == 'D':  # Debug data
            if not self._is_streaming:
                self._print_system_info()
                
        elif cmd_char == 'L':  # LED on
            GPIO.output(PIN_LED, GPIO.HIGH)
        elif cmd_char == 'l':  # LED off
            GPIO.output(PIN_LED, GPIO.LOW)
            
        elif cmd_char == 'S':  # Start streaming
            self._is_streaming = True
            self._motor.set_ready(False)
            print("Streaming started")
        elif cmd_char == 's':  # Stop streaming
            self._is_streaming = False
            self._motor.set_ready(True)
            print("Streaming stopped")
            
        elif cmd_char in ['Z', 'z']:  # Tare commands
            self._handle_tare_commands(cmd_char)
            
        elif cmd_char in ['C', 'c']:  # Calibration commands
            self._handle_calibration_commands(cmd_char)
            
        elif cmd_char in ['M', 'm', 'x']:  # Motor commands
            self._handle_motor_commands(cmd_char)
            
        elif cmd_char == 'T':  # Test sequence
            self._run_test_sequence()
            
        elif cmd_char == 'A':  # Alarm
            self._buzzer.beep(5)  # Play alarm tone
            '''case 'A':
                        // alarm
                        tone(PIN_BUZZ, 330, 500);
                        break; need to modify the tone()'''
            
        elif cmd_char == 'P':  # Play tone
            self._buzzer.beep(5)  # Play musical tone
            
        return True

    def _print_system_info(self):
        """Print system debug information"""
        print(f"\n--- System Info {VERSION} ---")
        print(f"Battery: {self._system.get_voltage():.2f}V")
        print(f"Charging: {'Yes' if self._system.get_charging() >= 200 else 'No'}")
        print(f"Fill Cell: zero={self._weight_fill.get_zero():.0f}, cal={self._weight_fill.get_cal():.2f}")
        print(f"Drain Cell: zero={self._weight_drain.get_zero():.0f}, cal={self._weight_drain.get_cal():.2f}")
        print("----------------------------")

    def _handle_tare_commands(self, cmd):
        """Process tare commands"""
        if cmd == 'Z':
            self._weight_fill.set_zero()
            print("Fill cell tared")
        else:
            self._weight_drain.set_zero()
            print("Drain cell tared")
        self._memory.save()

    def _handle_calibration_commands(self, cmd):
        """Process calibration commands"""
        if cmd == 'C':
            self._weight_fill.set_cal()
            print("Fill cell calibrated")
        else:
            self._weight_drain.set_cal()
            print("Drain cell calibrated")
        self._memory.save()

    def _handle_motor_commands(self, cmd):
        """Process motor control commands"""
        if cmd == 'M':
            self._motor.set_state(self._motor.State.UP.value)
            print("Motor UP")
        elif cmd == 'm':
            self._motor.set_state(self._motor.State.DOWN.value)
            print("Motor DOWN")
        else:
            self._motor.set_state(self._motor.State.STOP.value)
            print("Motor STOP")

    def _run_test_sequence(self):
        """Execute system test sequence"""
        print("Running test sequence...")
        GPIO.output(PIN_BUZZ, GPIO.HIGH)
        self._motor.set_state(self._motor.State.UP.value)
        time.sleep(1)
        self._motor.set_state(self._motor.State.DOWN.value)
        time.sleep(1)
        self._motor.set_state(self._motor.State.STOP.value)
        GPIO.output(PIN_BUZZ, GPIO.LOW)
        print("Test complete")

    def buffer_shift(self, buffer):
        """Shift buffer contents by one position"""
        for i in range(len(buffer)-1, 0, -1):
            buffer[i] = buffer[i-1]

    def cleanup(self):
        """Clean up resources"""
        if self._serial and self._serial.is_open:
            self._serial.close()
        GPIO.output(PIN_LED, GPIO.LOW)
        print("UART communication stopped")