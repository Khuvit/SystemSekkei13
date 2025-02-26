#include <BluetoothSerial.h>
#include "LED_control.h"

BluetoothSerial SerialBT;
bool isBlackTurn = true;  // Track current turn(kore daiji)

void setup() {
    Serial.begin(115200);
    if (!SerialBT.begin("ESP32_Othello")) {
        Serial.println("An error occurred initializing Bluetooth");
        while (1);
    }
    Serial.println("Bluetooth device started, waiting for connections...");
    initLEDs(); 
}

void loop() {
    if (SerialBT.available()) {
        String move = SerialBT.readStringUntil('\n');
        move.trim(); 

        Serial.print("Received move: ");
        Serial.println(move);

        if (move.length() == 2) {
            Serial.print("Processing move: ");
            Serial.println(move);

            updateLEDsForMove(move, isBlackTurn);

            Serial.println("LED update function called.");
            
            isBlackTurn = !isBlackTurn;
        } else {
            Serial.println("Invalid move format received.");
        }
    }
    delay(20);
}
