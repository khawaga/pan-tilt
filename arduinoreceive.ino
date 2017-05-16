#include <Servo.h>
Servo servoTilt, servoPan;

void setup() {
  servoPan.attach(3);
  servoPan.write(90);
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
}
void loop() {
 while(Serial.available()) {
   char buffer[7];
   Serial.readBytesUntil('n',buffer,7);
   int incomingValue = atoi(buffer);
   Serial.println(incomingValue);
   servoPan.write(incomingValue);
   delay(100); // delay for 1/10 of a second
 }
}
