#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <LiquidCrystal.h>
float temperature;
float humidity;
float pressure;
static byte state;
unsigned long time_start;

#define ALTITUDE 216.0 // Altitude in Sparta, Greece
#define ILLU_BUTTON 10
#define ILLU_CONTROL 9
#define STATE_ILLU_OFF 0
#define STATE_ILLU_ON 1

Adafruit_BME280 bme; // I2C

// LiquidCrystal (rs, enable, d4, d5, d6, d7)
LiquidCrystal lcd(8, 7, 3, 4, 5, 6);


void setup(void) {
  pinMode(ILLU_BUTTON, INPUT_PULLUP);
  pinMode(ILLU_CONTROL, OUTPUT);
  digitalWrite(ILLU_CONTROL, LOW);
  state = STATE_ILLU_OFF;
  
  lcd.begin(16, 2);
  lcd.print("Reading sensor");
  bool status;
    
    // default settings
    status = bme.begin(0x76);  //The I2C address of the sensor I use is 0x76
    if (!status) {
        lcd.clear();
        lcd.print("Error. Check");
        lcd.setCursor(0,1);
        lcd.print("connections");
        while (1);
    }
}
void loop() {
 
 delay(2000);
 getPressure();
 getHumidity();
 getTemperature();
 
 lcd.clear();
 
 //Printing Temperature
 String temperatureString = String(temperature,1);
 lcd.print("T:");
 lcd.print(temperatureString);
 lcd.print((char)223);
 lcd.print("C ");
 
 //Printing Humidity
 String humidityString = String(humidity,0);
 lcd.print("H: ");
 lcd.print(humidityString);
 lcd.print("%");
 
 //Printing Pressure
 lcd.setCursor(0,1);
 lcd.print("P: ");
 String pressureString = String(pressure,2);
 lcd.print(pressureString);
 lcd.print(" hPa");

 // button stuff
 if ((state == STATE_ILLU_OFF) && (digitalRead(ILLU_BUTTON) == LOW)) {
    time_start = millis();
    digitalWrite(ILLU_CONTROL, HIGH);
    state = STATE_ILLU_ON;
 } else if (state == STATE_ILLU_ON) {
    if (digitalRead(ILLU_BUTTON) == LOW) {
        time_start = millis();    
    } else {
        if (millis() - time_start > 3000) {
            digitalWrite(ILLU_CONTROL, LOW);
            state = STATE_ILLU_OFF;
        }
    }
 }
 
}

float getTemperature() {
  temperature = bme.readTemperature();
}

float getHumidity() {
  humidity = bme.readHumidity();
}

float getPressure() {
  pressure = bme.readPressure();
  pressure = bme.seaLevelForAltitude(ALTITUDE, pressure);
  pressure = pressure/100.0F;
}
