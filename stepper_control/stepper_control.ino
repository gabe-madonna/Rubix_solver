/*
Adafruit Arduino - Lesson 16. Stepper
*/
#include <Stepper.h>

Stepper init_motor(int pin_array[])
{
  Stepper motor(512, pin_array[1], pin_array[2], pin_array[3], pin_array[4]);
  return motor;
}

int pinsU[4] = {12, 11, 10, 9};
int pinsD[4] = {12, 11, 10, 9};
int pinsL[4] = {12, 11, 10, 9};
int pinsR[4] = {12, 11, 10, 9};
int pinsF[4] = {12, 11, 10, 9};
int pinsB[4] = {12, 11, 10, 9};
int pins[6] = {pinsU, pinsD, pinsL, pinsR, pinsF, pinsB};

Stepper motU = init_motor(pinsU);
Stepper motD = init_motor(pinsD);
Stepper motL = init_motor(pinsL);
Stepper motR = init_motor(pinsR);
Stepper motF = init_motor(pinsF);
Stepper motB = init_motor(pinsB);
Stepper motors[6] = {motU, motD, motL, motR, motF, motB};

void setup()
{
  for (int motor = 0; motor < 6; motor++)
  {
    for (int pin = 0; pin < 4; pin++)
    {
      pinMode(pins[motor, pin], OUTPUT);
    }
  }
  // this line delays the serial interface
  // until the terminal window is opened
  while (!Serial);
  Serial.begin(115200);
  for (int motor = 0; motor < 6; motor++)
  {
    motors[motor].setSpeed(50);
  }
}

String faces = "UDLRFB";
int steps_per_quart = 512;

void loop()
{
  String face = "";
  int quar_turns = 0;
  int steps = 0;
  int motor = 0;
  if (Serial.available())
  {
    String input = Serial.readString();
    face = input.substring(1);
    quar_turns = input.substring(1, input.length()).toInt();
    steps = quar_turns * steps_per_quart;
    motor = faces.indexOf(face);
    motors[motor].step(steps);
  }
}
