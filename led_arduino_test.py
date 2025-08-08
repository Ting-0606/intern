import serial
import serial.tools.list_ports
import sys
import struct

class CameraLEDController:
    def __init__(self):
        self.serialInst = None
        self.BAUDRATE = 115200
        
    
    def setup_device_serial(self):
        """Connect to Arduino with port selection and verification"""
        self.serialInst = serial.Serial()
        
        # Linux port detection
        if not sys.platform.startswith('win'):
            ports = serial.tools.list_ports.comports()
            available_ports = []
            
            print("\nAvailable serial ports:")
            for i, port in enumerate(ports, 1):
                print(f"{i}. {port.device} - {port.description}")
                available_ports.append(port.device)
            
            if not available_ports:
                print("No serial ports found!")
                return None
                
            if len(available_ports) == 1:
                print(f"\nAuto-selecting {available_ports[0]} (only port found)")
                self.serialInst.port = available_ports[0]
            else:
                while True:
                    try:
                        choice = int(input("\nSelect port number (1-{}): ".format(len(available_ports))))
                        if 1 <= choice <= len(available_ports):
                            self.serialInst.port = available_ports[choice-1]
                            break
                        else:
                            print("Invalid selection!")
                    except ValueError:
                        print("Please enter a number")

        self.serialInst.baudrate = self.BAUDRATE
        self.serialInst.timeout = 1
        
        try:
            self.serialInst.open()
            if self.serialInst.is_open:
                print(f"Serial port {self.serialInst.port} opened successfully")
                return True
            else:
                print(f"Failed to open serial port")
                return False
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")
            return False
    
    def make_package(self, cmd):
        """Create a command package with checksum"""
        checksum = ~(ord(cmd) + 1) % 256
        package = [255, 255, ord(cmd), 1, checksum]
        return b''.join(struct.pack('B', pack) for pack in package)
    
    def press_button_led(self):
        """Turn camera LED ON"""
        if self.serialInst and self.serialInst.is_open:
            self.serialInst.write(self.make_package('L'))
            print("LED turned ON")
        else:
            print("Serial port not available")
    
    def release_button_led(self):
        """Turn camera LED OFF"""
        if self.serialInst and self.serialInst.is_open:
            self.serialInst.write(self.make_package('l'))
            print("LED turned OFF")
        else:
            print("Serial port not available")
    
    def run(self):
        """Main interactive loop"""
        if not self.setup_device_serial():
            return
        
        print("Camera LED Controller")
        print("Commands:")
        print("  L - Turn LED ON")
        print("  l - Turn LED OFF")
        print("  q - Quit")
        
        while True:
            command = input("Enter command: ").strip()
            if command == 'L':
                self.press_button_led()
            elif command == 'l':
                self.release_button_led()
            elif command.lower() == 'q':
                print("Exiting...")
                if self.serialInst and self.serialInst.is_open:
                    self.serialInst.close()
                break
            else:
                print("Invalid command. Use 'L', 'l', or 'q'.")

if __name__ == "__main__":
    controller = CameraLEDController()
    controller.run()