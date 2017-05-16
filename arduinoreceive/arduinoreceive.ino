#include <Servo.h>
Servo servoTilt, servoPan;
int val;

void setup() {
  servoTilt.attach(2);
  servoTilt.write(90);
  servoPan.attach(3);
  servoPan.write(90);
  Serial.begin(57600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
}
void loop() {
 if (Serial.available() > 0) {
   char serialChar = Serial.read();
   if (serialChar == 't') {
     val = Serial.read();
     Serial.print(serialChar);
     Serial.print(val);
     Serial.print('\n');
     servoTilt.write(val);
   }
   else if (serialChar == 'p') {
     val = Serial.read();
     Serial.print(serialChar);
     Serial.print(val);
     Serial.print('\n');
     servoPan.write(val);
   }
 }
 delay(50); // delay for 1/10 of a second
}
