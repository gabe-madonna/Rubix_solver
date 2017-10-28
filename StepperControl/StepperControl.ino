/*
Adafruit Arduino - Lesson 16. Stepper
*/

#include <Stepper.h>

int in1Pin = 12;
int in2Pin = 11;
int in3Pin = 10;
int in4Pin = 9;

Stepper motor1(512, in1Pin, in2Pin, in3Pin, in4Pin);
//Stepper motor2(512, in1Pin, in2Pin, in3Pin, in4Pin);
//Stepper motor3(512, in1Pin, in2Pin, in3Pin, in4Pin);
//Stepper motor4(512, in1Pin, in2Pin, in3Pin, in4Pin);
//Stepper motor5(512, in1Pin, in2Pin, in3Pin, in4Pin);
//Stepper motor6(512, in1Pin, in2Pin, in3Pin, in4Pin);  

void setup()
{
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);

  // this line is for Leonardo's, it delays the serial interface
  // until the terminal window is opened
  while (!Serial);
  
  Serial.begin(9600);
  motor1.setSpeed(10);
}

void loop()
{
  if (Serial.available())
  {
    int steps = Serial.parseInt();
    motor1.step(steps);
  }
}
