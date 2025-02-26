#include "LED_control.h"
#include <FastLED.h>

#define LED_PIN 12
#define NUM_LEDS 64
CRGB leds[NUM_LEDS];

void initLEDs() {
    FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
    FastLED.clear();
    FastLED.show();  
    
    FastLED.show();
    Serial.println("LED board cleared and initialized with green fields.");
}

void updateLEDsForMove(String move, bool isBlack) {
    if (move.length() < 2) {
        Serial.println("Invalid move format.");
        return;
    }

    // Convert column letter (A-H -> 0-7)
    char colChar = toupper(move.charAt(0));
    int col = colChar - 'A';

    // Convert row number (1-8 -> 0-7)
    int row = move.substring(1).toInt() - 1;

    // Validate position
    if (col < 0 || col >= 8 || row < 0 || row >= 8) {
        Serial.println("Move out of range.");
        return;
    }

    // Convert row/col to LED index based on standard layout
    int ledIndex;
    if (row % 2 == 0) {
        ledIndex = row * 8 + col;  // Even rows: left to right
    } else {
        ledIndex = (row + 1) * 8 - (col + 1);  // Odd rows: right to left (Zig-Zag fix)
    }

    // mapping---->
    Serial.print("Move: ");
    Serial.print(move);
    Serial.print(" | Row: ");
    Serial.print(row);
    Serial.print(" Col: ");
    Serial.print(col);
    Serial.print(" | LED Index: ");
    Serial.println(ledIndex);

    if (isBlack) {
        leds[ledIndex] = CRGB(64, 0, 0);  // Red for black pieces
    } else {
        leds[ledIndex] = CRGB(255, 255, 255);  // White for white pieces
    }

    FastLED.show();
    
    Serial.print("LED at ");
    Serial.print((char)(col + 'A'));
    Serial.print(row + 1);
    Serial.print(" turned ");
    Serial.println(isBlack ? "Red (Black Piece)" : "White (White Piece)");
}