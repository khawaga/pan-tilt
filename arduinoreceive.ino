#include <Servo.h>
Servo servoTilt, servoPan;

void setup() {
  servoTilt.attach(2);
  servoTilt.write(90);
  servoPan.attach(3);
  servoPan.write(90);
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
}
void loop() {
 while(Serial.available()) {
   char buffer[7];
   char first = Serial.read();
   if (first == 'p') {
     Serial.readBytesUntil('\n',buffer,7);
     int incomingValue = atoi(buffer);
     if (incomingValue >= 0 && incomingValue <= 180) {
       Serial.println(incomingValue);
       servoPan.write(incomingValue);
     }
   }
   if (first == 't') {
     Serial.readBytesUntil('\n',buffer,7);
     int incomingValue = atoi(buffer);
     if (incomingValue >= 0 && incomingValue <= 180) {
       Serial.println(incomingValue);
       servoTilt.write(incomingValue);
     }
   }
   delay(100); // delay for 1/10 of a second
 }
}
