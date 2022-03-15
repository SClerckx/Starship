#include <SPI.h>
#include <LoRa.h>

int counter = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }else{
     Serial.println("Starting LoRa succesful");
  }
  LoRa.setTxPower(20);
}

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);

  // send packet
  
  LoRa.beginPacket();
  Serial.print("beginPacket ");
  LoRa.print("hello ");
  Serial.print("hello ");
  LoRa.print(counter);
  Serial.print("Counter ");
  LoRa.endPacket();
  Serial.print("endPacket ");

  counter++;

  delay(5000);
}
