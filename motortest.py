#!/usr/bin/env python3
import sys
from A4950_V2 import A4950
import RPi.GPIO as GPIO
import time

def verify_pin_states(motor, expected_in0, expected_in1, expected_led):
    """Physically verify the pin states match expected values"""
    print("\nVerifying actual pin voltages:")
    
    # Read actual pin states
    actual_in0 = GPIO.input(motor._pin_a4950_in0)
    actual_in1 = GPIO.input(motor._pin_a4950_in1)
    actual_led = GPIO.input(motor._pin_a4950_led)
    
    # Print verification results
    print(f"IN0 (M0): Expected {'HIGH' if expected_in0 else 'LOW'} | Actual {'HIGH' if actual_in0 else 'LOW'} {'✓' if actual_in0 == expected_in0 else '✗'}")
    print(f"IN1 (M1): Expected {'HIGH' if expected_in1 else 'LOW'} | Actual {'HIGH' if actual_in1 else 'LOW'} {'✓' if actual_in1 == expected_in1 else '✗'}")
    print(f"LED: Expected {'HIGH' if expected_led else 'LOW'} | Actual {'HIGH' if actual_led else 'LOW'} {'✓' if actual_led == expected_led else '✗'}")
    
    # Verify switches
    sw0_state =  GPIO.input(motor._pin_sw_0)  
    sw1_state =  GPIO.input(motor._pin_sw_1)
    print(f"SW_0: {'noPRESSED' if sw0_state else ' PRESSED'}") #sw0_state is a boolean, 1=T, 0=F
    print(f"SW_1: {'noPRESSED' if sw1_state else ' PRESSED'}")
    print(sw0_state)
    print(sw1_state)

def main():
    # Initialize motor controller
    motor = A4950()
    motor.init()  # Using default pins
    
    try:
        motor.set_ready(True)
        print("A4950 Motor Controller Test - Voltage Verification")
        print("------------------------------------------------")
        
        while True:
            print("\nOptions:")
            print("1. Move UP (verify IN0=HIGH, IN1=LOW, LED=HIGH)")
            print("2. Move DOWN (verify IN0=LOW, IN1=HIGH, LED=HIGH)")
            print("3. STOP (verify IN0=LOW, IN1=LOW, LED=LOW)")
            print("4. Check switch status")
            print("5. Check if motor is moving")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == '1':
                motor.set_state(motor.State.UP.value)
                print("\nCommand: Move UP")
                verify_pin_states(motor, True, False, True)
            elif choice == '2':
                motor.set_state(motor.State.DOWN.value)
                print("\nCommand: Move DOWN")
                verify_pin_states(motor, False, True, True)
            elif choice == '3':
                motor.set_state(motor.State.STOP.value)
                print("\nCommand: STOP")
                verify_pin_states(motor, False, False, False)
            elif choice == '4':
                motor.check_switch()
                print("\nSwitch Status Check:")

                verify_pin_states(motor, 
                                 GPIO.input(motor._pin_a4950_in0),
                                 GPIO.input(motor._pin_a4950_in1),
                                 GPIO.input(motor._pin_a4950_led))
            elif choice == '5':
                print(f"\nMotor is moving: {'Yes' if motor.get_is_moving() else 'No'}")
                
                '''verify_pin_states(motor,
                                GPIO.input(motor._pin_a4950_in0),
                                GPIO.input(motor._pin_a4950_in1),
                                GPIO.input(motor._pin_a4950_led))'''
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1-6.")
                
            time.sleep(0.5)  # Allow time for voltage stabilization
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        motor.cleanup()
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()