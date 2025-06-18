import time
import RPi.GPIO as GPIO
from setup import *
from hx711 import HX711
from a4950 import A4950
from system_monitor import System
from memory import Memory
from uart_comms import UART
from sound import Sound

def main():
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BLE_CONNECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Initialize all components
    print(f"Initializing system {VERSION}...")
    buzz = Sound(PIN_BUZZ)
    weight_fill = HX711(HX711_DOUT_FILL, HX711_PD_SCK_FILL)
    weight_drain = HX711(HX711_DOUT_DRAIN, HX711_PD_SCK_DRAIN)
    motor = A4950()
    sys = System()
    mem = Memory(weight_fill, weight_drain)
    ble = UART(weight_fill, weight_drain, motor, sys, mem, buzz)

    # Initialize timers
    timer1 = time.time() * 1000000  # microseconds
    timer2 = timer1
    toggle = False

    try:
        # Setup components
        print("Initializing components...")
        ble.init(BAUDRATE)
        sys.init(PIN_BATTERY, PIN_CHARGE_ADC, PIN_CHARGING, PIN_CAM)
        weight_fill.init()
        weight_drain.init()
        mem.init()
        motor.init(A4950_IN0, A4950_IN1, A4950_LED, MOTOR_SWITCH_0, MOTOR_SWITCH_1)
        motor.set_ready(True)
        
        print("System ready. Starting main loop...")
        
        # Main control loop
        while True:
            current_time = time.time() * 1000000  # microseconds

            # High-frequency tasks (20Hz)
            if current_time - timer1 >= LOOP_TIME:
                # Check Bluetooth connection status
                ble.check_connection(BLE_CONNECT)
                
                # Monitor battery status
                sys.check_battery()
                
                # Process incoming UART commands
                ble.data_receive()
                
                # Check motor limit switches
                motor.check_switch()
                
                # Send data if streaming
                ble.data_send()
                
                timer1 = current_time

            # Low-frequency tasks (1Hz)
            if current_time - timer2 >= ONE_SEC:
                # Toggle buzzer if motor is moving
                toggle = not toggle if motor.get_is_moving() else False
                if toggle:
                    buzz.beep(5)  # Play tone
                
                timer2 = current_time

            # Small delay to prevent CPU overload
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup resources
        ble.cleanup()
        motor.cleanup()
        sys.cleanup()
        GPIO.cleanup()
        print("System shutdown complete.")

if __name__ == "__main__":
    main()