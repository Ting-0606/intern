#include <Arduino.h>
#include "HX711.h"

HX711::HX711() {};

void HX711::init(int pin_dout, int pin_pd_sck) {
    _pin_dout = pin_dout;
    _pin_pd_sck = pin_pd_sck;
    pinMode(_pin_dout, INPUT);
    pinMode(_pin_pd_sck, OUTPUT);
}

unsigned long HX711::read() {
    unsigned long count = 0; 

    // when output data is not ready for retrieval
    // digital output pin DOUT is high
    // serial clock input should be low
	digitalWrite(_pin_dout, HIGH);
	delayMicroseconds(1);
	digitalWrite(_pin_pd_sck, LOW);
	delayMicroseconds(1);

  	
    // when DOUT goes to low, it indictes data is ready for retrieval
	while(digitalRead(_pin_dout));

    // by applying 25-27 positive clock pulses at the PD_SCK pin
    // data is shifted out from the DOUT output pin
    // each pulse shifts out one bit, starting at MSB bit first
    // until all 24 bits are shifted out
	for(int i = 0; i < 24; i++){ 
		// pulse high
        digitalWrite(_pin_pd_sck, HIGH); 
		delayMicroseconds(1);
		
        // shift the bit too the left
        count = count << 1; 
		
        // pulse low
        digitalWrite(_pin_pd_sck, LOW); 
		delayMicroseconds(1);

        // data out, registered at the right-most bit
		if(digitalRead(_pin_dout))
			count++; 
	} 

    // the 25th bit will pull DOUT pin back to high
	digitalWrite(_pin_pd_sck, HIGH); 
	delayMicroseconds(1);
	digitalWrite(_pin_pd_sck, LOW); 
	delayMicroseconds(1);
	
    // the output 24 bits of data is in 2's complement format
    // when goes out of range, output data will be saturated at 800000h (min) or 7fffffh (max)
	count ^= 0x800000;
	return count;
}

unsigned long HX711::set_zero() {
    // get ADC reading at zero weight
    _zero = read();
    return _zero;
}

unsigned long HX711::get_zero() {
    return _zero;
}

unsigned long HX711::set_cal() {
    // get ADC reading at 1kg weight
    _cal = (read() - _zero) / 1000.0;
    return _cal;
}

unsigned long HX711::get_cal() {
    return _cal;
}

void HX711::input_zero(float val) {
    _zero = val;
}

void HX711::input_cal(float val) {
    _cal = val;
}

float HX711::get_weight() {
    // compute calibrated weighted load cell
    weight = (float) ((read() - _zero) / _cal);
    return weight;
}
