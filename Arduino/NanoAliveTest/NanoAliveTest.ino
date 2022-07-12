#include "Arduino.h"

void setup() {
  Serial.begin(9600);
  Serial.println("START");

  // To set the radioNumber via the Serial monitor on startup
  Serial.println(F("Which radio is this? Enter '0' or '1'. Defaults to '0'"));
  while (!Serial.available()) {
    // wait for user input
  }
}

void loop() {
  Serial.println("listening");
}
