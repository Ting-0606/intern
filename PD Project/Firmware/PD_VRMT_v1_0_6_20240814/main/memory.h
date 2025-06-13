#ifndef __MEMORY_H__
#define __MEMORY_H__

#include "setup.h"
#include "HX711.h"

#define CONFIG_DEFAULT          10
#define CONFIG_START            100

class Memory {
    private:
        struct {
            char version[10];
            float fill_zero;
            float fill_cal; 
            float drain_zero;
            float drain_cal;
        } _mem;
        
        HX711* _ptr_weight_fill;
        HX711* _ptr_weight_drain;

    public:
        Memory(HX711* weight_fill, HX711* weight_drain);

        void init();
        void reset();
        void load();
        void load(int loc);
        void save();
        void save(int loc);
};

#endif