// Basic demo for readings from Adafruit BNO08x
#include <Adafruit_BNO08x.h>

// For SPI mode, we need a CS pin
#define BNO08X_CS 10
#define BNO08X_INT 9

// For SPI mode, we also need a RESET 
//#define BNO08X_RESET 5
// but not for I2C or UART
#define BNO08X_RESET -1

Adafruit_BNO08x  bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;

void setup(void) {
  Serial.begin(115200);
  while (!Serial) delay(10);     // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit BNO08x test!");

  // Try to initialize!
  if (!bno08x.begin_I2C()) {
  //if (!bno08x.begin_UART(&Serial1)) {  // Requires a device with > 300 byte UART buffer!
  //if (!bno08x.begin_SPI(BNO08X_CS, BNO08X_INT)) {
    Serial.println("Failed to find BNO08x chip");
    while (1) { delay(10); }
  }
  Serial.println("BNO08x Found!");

  for (int n = 0; n < bno08x.prodIds.numEntries; n++) {
    Serial.print("Part ");
    Serial.print(bno08x.prodIds.entry[n].swPartNumber);
    Serial.print(": Version :");
    Serial.print(bno08x.prodIds.entry[n].swVersionMajor);
    Serial.print(".");
    Serial.print(bno08x.prodIds.entry[n].swVersionMinor);
    Serial.print(".");
    Serial.print(bno08x.prodIds.entry[n].swVersionPatch);
    Serial.print(" Build ");
    Serial.println(bno08x.prodIds.entry[n].swBuildNumber);
  }

  setReports();

  Serial.println("Reading events");
  delay(100);
}

// Here is where you define the sensor outputs you want to receive
void setReports(void) {
  Serial.println("Setting desired reports");
  /*if (! bno08x.enableReport(SH2_GAME_ROTATION_VECTOR)) {
    Serial.println("Could not enable game vector");
  }*/
  if (! bno08x.enableReport(SH2_ROTATION_VECTOR)) {
    Serial.println("Could not enable rotation vector");
  }
  if (! bno08x.enableReport(SH2_GYROSCOPE_CALIBRATED)) {
    Serial.println("Could not enable gyroscope");
  }
}


void loop() {
  //delay(10);

  if (bno08x.wasReset()) {
    Serial.print("sensor was reset ");
    setReports();
  }
  
  if (! bno08x.getSensorEvent(&sensorValue)) {
    return;
  }
  
  switch (sensorValue.sensorId) {
    
    /*case SH2_GAME_ROTATION_VECTOR:
      Serial.print(" rgame:");
      Serial.print(sensorValue.un.gameRotationVector.real);
      Serial.print(" igame:");
      Serial.print(sensorValue.un.gameRotationVector.i);
      Serial.print(" jgame:");
      Serial.print(sensorValue.un.gameRotationVector.j);  
      Serial.print(" kgame:");
      Serial.println(sensorValue.un.gameRotationVector.k);
      ///Serial.print("\n");
      break;*/
    
    /*case SH2_ROTATION_VECTOR:
      Serial.print(" rrotation:");
      Serial.print(sensorValue.un.rotationVector.real);
      Serial.print(" irotation:");
      Serial.print(sensorValue.un.rotationVector.i);
      Serial.print(" jrotation:");
      Serial.print(sensorValue.un.rotationVector.j);
      Serial.print(" krotation:");
      Serial.println(sensorValue.un.rotationVector.k);
      break;*/

    case SH2_GYROSCOPE_CALIBRATED:
      Serial.print(" x:");
      Serial.print(sensorValue.un.gyroscope.x);
      Serial.print(" y:");
      Serial.print(sensorValue.un.gyroscope.y);
      Serial.print(" z:");
      Serial.println(sensorValue.un.gyroscope.z);
      break;
  }

}
