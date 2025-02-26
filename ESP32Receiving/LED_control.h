#ifndef LED_CONTROL_H
#define LED_CONTROL_H

#include <Arduino.h>

void initLEDs();

void updateLEDsForMove(String move, bool isBlack);

#endif
