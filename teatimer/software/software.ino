/* teatimer code */

#include <EEPROM.h>
#include <LiquidCrystal.h>
#include <FTDebouncer.h>


#define VERSIONSTR "teatimer 1.0.0"

// different states of state machine
# define WAITMODE 0
# define MINMODE 1
# define SECMODE 2
# define RUNMODE 3
# define PAUSEMODE 4
# define ALERTMODE 5

#define BTNLEFT 9
#define BTNMIDDLE 8
#define BTNRIGHT 7
unsigned char MODE = WAITMODE;
unsigned char value_minute, value_minute_save;
char value_second, value_second_save;
unsigned long last_millis;
bool blink;
#define VALUE_MINUTE_MAX 255
#define VALUE_SECOND_MAX 59
#define EEPROM_ADDRESS_MINUTE 0
#define EEPROM_ADDRESS_SECOND 1
#define USE_EEPROM
char BUFFER[20];
#define SPEAKER 10

// initialize LCD interface 
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
FTDebouncer pinDebouncer(30);

void onPinActivated(int btnNumber){
    if (MODE == WAITMODE) {
        if (btnNumber == BTNLEFT) {
            // 'Min' button pressed
            MODE = MINMODE;
            lcd.clear();
            updateMinute();
            setLCDUpDownOk();
        } else if (btnNumber == BTNMIDDLE) {
            // 'Sec' button pressed
            MODE = SECMODE;
            lcd.clear();
            updateSecond();
            setLCDUpDownOk();
        } else if (btnNumber == BTNRIGHT) {
            // 'Start' button pressed
            MODE = RUNMODE;
            setLCDResetPauseStop();
            if (value_minute == 0 && value_second == 0) {
                value_minute = VALUE_MINUTE_MAX;
                value_second = VALUE_SECOND_MAX;
            }
            value_minute_save = value_minute;
            value_second_save = value_second;
            #ifdef USE_EEPROM
            if (EEPROM.read(EEPROM_ADDRESS_MINUTE) != value_minute_save) {
                EEPROM.write(EEPROM_ADDRESS_MINUTE, value_minute_save);
            }
            if (EEPROM.read(EEPROM_ADDRESS_SECOND) != value_second_save) {
                EEPROM.write(EEPROM_ADDRESS_SECOND, value_second_save);
            }
            #endif
            last_millis = millis();
            updateLCD();
        }
    } 
    else if (MODE == MINMODE) {
        if (btnNumber == BTNLEFT) {
            // up pressed
            if (value_minute >= VALUE_MINUTE_MAX) {
                value_minute = 0;
            } else {
                value_minute += 1;
            }
            updateMinute();
        } 
        else if (btnNumber == BTNMIDDLE) {
            // down pressed
            if (value_minute <= 0) {
                value_minute = VALUE_MINUTE_MAX;
            } else {
                value_minute -= 1;
            }
            updateMinute();
        } 
        else if (btnNumber == BTNRIGHT) {
            // ok pressed
            updateLCD();
            setLCDMinSecStart();
            MODE = WAITMODE;
        }
    }
    else if (MODE == SECMODE) {
        if (btnNumber == BTNLEFT) {
            // up pressed
            if (value_second >= VALUE_SECOND_MAX) {
                value_second = 0;
            } else {
                value_second += 1;
            }
            updateSecond();
        } 
        else if (btnNumber == BTNMIDDLE) {
            // down pressed
            if (value_second <= 0) {
                value_second = VALUE_SECOND_MAX;
            } else {
                value_second -= 1;
            }
            updateSecond();
        } 
        else if (btnNumber == BTNRIGHT) {
            // ok pressed
            updateLCD();
            setLCDMinSecStart();
            MODE = WAITMODE;
        }
    }
    else if (MODE == ALERTMODE) {
        // any button pressed
        value_minute = value_minute_save;
        value_second = value_second_save;
        lcd.display();
        noTone(SPEAKER);
        updateLCD();
        setLCDMinSecStart();
        MODE = WAITMODE;
    }
    else if (MODE == RUNMODE) {
        if (btnNumber == BTNLEFT) {
            // 'Reset' button pressed
            MODE = WAITMODE;
            value_minute = 0;
            value_second = 0;
            setLCDMinSecStart();
            updateLCD();
        } else if (btnNumber == BTNMIDDLE) {
            // 'Pause' button pressed
            MODE = PAUSEMODE;
            setLCDResetContStop();
        } else if (btnNumber == BTNRIGHT) {
            // 'Stop' button pressed
            MODE = WAITMODE;
            value_minute = value_minute_save;
            value_second = value_second_save;
            setLCDMinSecStart();
            updateLCD();
        }
    }
    else if (MODE == PAUSEMODE) {
        if (btnNumber == BTNLEFT) {
            // 'Reset' button pressed
            MODE = WAITMODE;
            value_minute = 0;
            value_second = 0;
            setLCDMinSecStart();
            updateLCD();
        } else if (btnNumber == BTNMIDDLE) {
            // 'Cont' button pressed
            MODE = RUNMODE;
            setLCDResetPauseStop();
        } else if (btnNumber == BTNRIGHT) {
            // 'Stop' button pressed
            MODE = WAITMODE;
            value_minute = value_minute_save;
            value_second = value_second_save;
            setLCDMinSecStart();
            updateLCD();
        }
    }
    digitalWrite(LED_BUILTIN, HIGH);
}

void onPinDeactivated(int pinNumber){
    // do something according to the _pinNR that is triggered
    // for instance:
    digitalWrite(LED_BUILTIN, LOW);
}

void updateLCD() {
    sprintf(BUFFER, "%03d:%02d          ", value_minute, value_second);  // trailing spaces at end are needed to delete previous data
    lcd.setCursor(0, 0);
    lcd.print(BUFFER);
}

void updateMinute() {
    sprintf(BUFFER, "Min %03d", value_minute);
    lcd.setCursor(0, 0);
    lcd.print(BUFFER);
}

void updateSecond() {
    sprintf(BUFFER, "Sec %02d", value_second);
    lcd.setCursor(0, 0);
    lcd.print(BUFFER);
}

void setLCDResetContStop() {
    lcd.setCursor(0, 1);
            // 00000000011111111
            // 12345678901234456
    lcd.print("Reset Cont  Stop");
}

void setLCDResetPauseStop() {
    lcd.setCursor(0, 1);
            // 00000000011111111
            // 12345678901234456
    lcd.print("Reset Pause Stop");
}

void setLCDMinSecStart() {
    lcd.setCursor(0, 1);
            // 00000000011111111
            // 12345678901234456
    lcd.print("Min   Sec  Start");
}

void setLCDUpDownOk() {
    lcd.setCursor(0, 1);
            // 00000000011111111
            // 12345678901234456
    lcd.print("Up   Down    OK");
}

void setLCDOkOkOk() {
    lcd.setCursor(0, 1);
            // 00000000011111111
            // 12345678901234456
    lcd.print("OK   OK      OK ");
}

void setup() {
    pinMode(SPEAKER, OUTPUT);
    Serial.begin(57600);

    #ifdef USE_EEPROM
    value_minute = EEPROM.read(EEPROM_ADDRESS_MINUTE);
    value_second = EEPROM.read(EEPROM_ADDRESS_SECOND);
    #endif

    // set up LCD
    lcd.begin(16, 2);
    lcd.setCursor(0, 0);
    lcd.print(VERSIONSTR);
    lcd.setCursor(0, 1);
    sprintf(BUFFER, "Accu=%d", analogRead(A0));
    lcd.print(BUFFER);
    delay(2000);
    lcd.clear();
    
    updateLCD();
    setLCDMinSecStart();

    // setup buttons
    pinDebouncer.addPin(7, HIGH, INPUT_PULLUP); // internal pull-up resistor 
    pinDebouncer.addPin(8, HIGH, INPUT_PULLUP); // internal pull-up resistor 
    pinDebouncer.addPin(9, HIGH, INPUT_PULLUP); // internal pull-up resistor 
    pinDebouncer.begin();
}

void loop() {
    pinDebouncer.update();
    if ((MODE == RUNMODE) && (millis() - last_millis >= 1000)) {
        last_millis = millis();
        if (value_minute > 0 || value_second > 0) {
            value_second -= 1;
            if (value_second < 0 && value_minute > 0) {
                value_minute -= 1;
                value_second = 59;
            }
            updateLCD();
        } else  {
            MODE = ALERTMODE;
            lcd.setCursor(0, 0);
            lcd.print("ALERT REACHED");
            setLCDOkOkOk();
        }
    } 
    else if (MODE == ALERTMODE) {
        if (millis() - last_millis >= 200) {
            last_millis = millis();
            blink = !blink;
            if (blink) {
                lcd.display();
                tone(SPEAKER, 230, 500);
            } else {
                lcd.noDisplay();
                noTone(SPEAKER);
            }

        }

    }
}

/*
set 'min', 'sec', 'start' caption
'min' pressed ->
    change caption 'min' to 'up'
    change caption 'sec' to 'down'
    change caption 'start' to 'ok'
    set value to 0
    'up' pressed -> 
        if value > max_minutes:
            set value to 0
        else
            value + 1
    'down' pressed ->
        if value == 0:
            set value to max_minutes
        else:
         value - 1
    'ok' pressed ->
        change caption 'up' to 'min'
        change caption 'down' to 'sec'
        change caption 'ok' to 'start'
        save value to min
        display min:sec
'sec' pressed ->
    change caption 'min' to 'up'
    change caption 'sec' to 'down'
    change caption 'start' to 'ok'
    set value to 0
    'up' pressed -> 
        if value > max_seconds:
            set value to 0
        else
            value + 1
    'down' pressed ->
        if value == 0:
            set value to max_seconds
        else:   
        value - 1
    'ok' pressed ->
        change caption 'up' to 'min'
        change caption 'down' to 'sec'
        change caption 'ok' to 'start'
        save value to sec
        display min:sec
'start' pressed ->
    change caption 'start' to 'stop'
    decrement min.sec 
    if min.sec == 0:
        alert
    'stop' pressed ->
        change caption 'stop' to 'start' 
        stop alert


*/
