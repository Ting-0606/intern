#include <Arduino.h>
#include <EEPROM.h>
#include "memory.h"
#include "HX711.h"

Memory::Memory(HX711* weight_fill, HX711* weight_drain) {
    _ptr_weight_fill = weight_fill;
    _ptr_weight_drain = weight_drain;
}

void Memory::init() {
    save(CONFIG_DEFAULT);
    load(CONFIG_START);
}

void Memory::reset() {
    load(CONFIG_DEFAULT);
}

void Memory::load() {
    load(CONFIG_START);
}

void Memory::load(int loc) {
    EEPROM.get(loc, _mem);
    if (strcmp(_mem.version, VERSION) == 0) {
        _ptr_weight_fill->input_zero(_mem.fill_zero);
        _ptr_weight_fill->input_cal(_mem.fill_cal);
        _ptr_weight_drain->input_zero(_mem.drain_zero);
        _ptr_weight_drain->input_cal(_mem.drain_cal);
    }
    else {
        save(CONFIG_START);
    }
}

void Memory::save() {
    save(CONFIG_START);
}

void Memory::save(int loc) {
    strcpy(_mem.version, VERSION);
    _mem.fill_zero = _ptr_weight_fill->get_zero();
    _mem.fill_cal = _ptr_weight_fill->get_cal();
    _mem.drain_zero = _ptr_weight_drain->get_zero();
    _mem.drain_cal = _ptr_weight_drain->get_cal();
    EEPROM.put(loc, _mem);
}
