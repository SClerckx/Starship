#include "Arduino.h"
#include <SPI.h>
#include <RF24.h>
#include <printf.h>

// This is just the way the RF24 library works:
// Hardware configuration: Set up nRF24L01 radio on SPI bus (pins 10, 11, 12, 13) plus pins 7 & 8
// https://github.com/RalphBacon/nRF24L01-transceiver/blob/master/nRF24L01_Test_Node_0/nRF24L01_Test_Node_0.ino
RF24 radio(7, 8);

byte addresses[][6] = {"1Node","2Node"};

long previousMillis = 0; 
long interval = 10000;  

// -----------------------------------------------------------------------------
// SETUP   SETUP   SETUP   SETUP   SETUP   SETUP   SETUP   SETUP   SETUP
// -----------------------------------------------------------------------------
void setup() {
  Serial.begin(9600);
  //while (!Serial.available()) {
    // wait for user input for Nano
  //}
  
  Serial.println("THIS IS THE RECEIVER CODE - YOU NEED THE OTHER ARDUINO TO TRANSMIT");

  // Initiate the radio object
  radio.begin();

  // Set the transmit power to lowest available to prevent power supply related issues
  radio.setPALevel(RF24_PA_MIN);

  // Set the speed of the transmission to the quickest available
  radio.setDataRate(RF24_1MBPS);

  // Use a channel unlikely to be used by Wifi, Microwave ovens etc
  radio.setChannel(124);

  // Open a writing and reading pipe on each radio, with opposite addresses
  radio.openWritingPipe(addresses[0]);
  radio.openReadingPipe(1, addresses[1]);

  delay(20);

  Serial.println("Details");
  // For debugging info
  printf_begin();             // needed only once for printing details
  radio.printDetails();       // (smaller) function that prints raw register values
  Serial.println("Pretty");
  radio.printPrettyDetails(); // (larger) function that prints human readable data
  
  // Start the radio listening for data
  radio.startListening();
  Serial.println("listening");
}

// -----------------------------------------------------------------------------
// We are LISTENING on this device only (although we do transmit a response)
// -----------------------------------------------------------------------------
void loop() {
   unsigned long currentMillis = millis();
 
  if(currentMillis - previousMillis > interval) 
  {
          Serial.println("listening details");
          // For debugging info
          //printf_begin();             // needed only once for printing details
          //radio.printDetails();       // (smaller) function that prints raw register values
          Serial.println("Pretty");
          radio.printPrettyDetails(); // (larger) function that prints human readable data
          // save the last time you blinked the LED 
          previousMillis = currentMillis;
  }
  
  // This is what we receive from the other device (the transmitter)
  unsigned char data;

  // Is there any data for us to get?
  if ( radio.available()) {

    // Go and read the data and put it into that variable
    while (radio.available()) {
      radio.read( &data, sizeof(char));
    }

    // No more data to get so send it back but add 1 first just for kicks
    // First, stop listening so we can talk
    radio.stopListening();
    data++;
    radio.write( &data, sizeof(char) );

    // Now, resume listening so we catch the next packets.
    radio.startListening();

    // Tell the user what we sent back (the random numer + 1)
    Serial.print("Sent response ");
    Serial.println(data);
  }
}
