import json
import os
from pathlib import Path

class Memory:
    CONFIG_DEFAULT = 10 
    CONFIG_START = 100 
    
    def __init__(self, weight_fill, weight_drain, version="1.0"):
        self._weight_fill = weight_fill
        self._weight_drain = weight_drain
        self._version = version
        self._config_file = Path.home() / ".hx711_calibration.json"
        self._mem = {
            'version': self._version,
            'fill_zero': 0.0,
            'fill_cal': 0.0,
            'drain_zero': 0.0,
            'drain_cal': 0.0
        }

    def init(self):
        self.save(self.CONFIG_DEFAULT)
        self.load(self.CONFIG_START)

    def reset(self):
        self.load(self.CONFIG_DEFAULT)

    def load(self, loc=None):     
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r') as f:
                    self._mem = json.load(f)
                
                if self._mem['version'] == self._version:
                    # Updated to use the new method names
                    self._weight_fill.input_zero_fill(self._mem['fill_zero'])
                    self._weight_fill.input_cal_fill(self._mem['fill_cal'])
                    self._weight_drain.input_zero_drain(self._mem['drain_zero'])
                    self._weight_drain.input_cal_drain(self._mem['drain_cal'])
                else:
                    self.save(self.CONFIG_START)
        except Exception as e:
            print(f"Error loading calibration: {e}")
            self.save(self.CONFIG_START)

    def save(self, loc=None):    
        try:
            self._mem = {
                'version': self._version,
                # Updated to use the new method names
                'fill_zero': self._weight_fill.get_zero_fill(),
                'fill_cal': self._weight_fill.get_cal_fill(),
                'drain_zero': self._weight_drain.get_zero_drain(),
                'drain_cal': self._weight_drain.get_cal_drain()
            }
            
            with open(self._config_file, 'w') as f:
                json.dump(self._mem, f, indent=4)
        except Exception as e:
            print(f"Error saving calibration: {e}")

    def get_config_path(self):
        return str(self._config_file)