#include <LiquidCrystal.h>

// LiquidCrystal(rs, enable, d4, d5, d6, d7)
LiquidCrystal lcd(8, 7, 6, 5, 4, 3);
bool wait;


void setup() {
    wait = true;
    pinMode(9,  INPUT_PULLUP);
    pinMode(10, INPUT_PULLUP);
    pinMode(11, INPUT_PULLUP);
    pinMode(12, INPUT_PULLUP);

    Serial.begin(115200);

    lcd.begin(16,2);
    lcd.print("Waiting ");
}



void loop() {
    if (wait == true) {
        lcd.setCursor(0, 1);
        lcd.print(millis() / 1000);
    }

    for (uint8_t which = 9; which <= 12; which++) {
        uint8_t btnBefore = digitalRead(which);
        delay(50);
        uint8_t btnAfter = digitalRead(which);
        if (btnBefore == LOW && btnAfter == LOW) {
            if (which == 9) {
                // volume down
                Serial.println("v-");
            }
            else if (which == 10) {
                // volume up
                Serial.println("v+");
            }
            else if (which == 11) {
                // next channel
                Serial.println("c+");
            }
            else {
                // previous channel
                Serial.println("c-");
            }
        }
    }

    if (Serial.available()) {
        wait = false;
        // read all the available characters
        while (Serial.available() > 0) {
            char c = Serial.read();
            // Serial.println(int(c));
            if (c == 3) {
                lcd.clear();
            }
            else if (c == 21) {
                // Ctrl-U: set cursor position row 0, column 0
                lcd.setCursor(0, 0);
            } else if (c == 22) {
                // Ctrl-V: set cursor position row 1, column 0
                lcd.setCursor(0, 1);
            } else {
                lcd.write(c);
            }
        }
    }
}
