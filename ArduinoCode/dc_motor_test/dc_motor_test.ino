#include <math.h>
#include <Stepper.h>
#include <Servo.h>

#define MIN_MOTOR_SPEED 100
#define FORWARD_DIR true
#define BACKWARD_DIR false

const double INPUT_MOTOR_RATIO = 255.0 / (255 - MIN_MOTOR_SPEED);  // Joystick ranges from 0-9, Motor ranges from MIN_SPEED-255

const float STEPS_PER_REV = 32;
const float GEAR_RED = 64;
const float STEPS_PER_OUT_REV = STEPS_PER_REV * GEAR_RED;

int stepsRequired;

// Stepper steppermotor(STEPS_PER_REV, 8, 10, 9, 11);
Servo myServo;

int servoPos = 92;

struct serialInput {
  int val = 0;
  char dir = 'X';
};

int speedPin = 5; 
int dir1Pin = 4;
int dir2Pin = 3;
int ledPin = 2;

char inputDir = 'S';

int motorSpeed = 0;
bool ledStatus = false;

// int potPin = A0;
// int potValue = 0;

void set_direction(bool dir) {
  if(dir == FORWARD_DIR){
    digitalWrite(dir1Pin, HIGH);
    digitalWrite(dir2Pin, LOW);
  } else {
    digitalWrite(dir1Pin, LOW);
    digitalWrite(dir2Pin, HIGH);
  }
}

serialInput getLastInput() {
  serialInput x;
  while(Serial.available()){
    char c = Serial.read();
    delay(1);
    if(c == 'F' || c == 'B'){
      x.dir = c;
      x.val = int(Serial.read());
      if(x.val == 0){
        x.dir = 'S'; // still
      }
    }
    // break;
  }
  return x;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(speedPin, OUTPUT);
  pinMode(dir1Pin, OUTPUT);
  pinMode(dir2Pin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  myServo.attach(9);
  myServo.write(45);

  digitalWrite(dir1Pin, HIGH);
  digitalWrite(dir2Pin, LOW);
  
  Serial.begin(9600);

  //stepsRequired = STEPS_PER_OUT_REV * 0.375;
  //steppermotor.setSpeed(500);
  //steppermotor.step(-stepsRequired);
  

  Serial.print("Ratio: "); Serial.println(INPUT_MOTOR_RATIO);
}

void loop() {
  // put your main code here, to run repeatedly:

  /*if(servoPos <= 180) {
    for(servoPos = 0; servoPos <= 180; servoPos++) {
      myServo.write(servoPos);
      delay(15);
    }
  } else {
    for(servoPos = 180; servoPos > 0; servoPos--) {
      myServo.write(servoPos);
      delay(15);
    }
  }*/

  if(Serial.available()){
    serialInput input = getLastInput();
    ledStatus = !ledStatus;
    //digitalWrite(ledPin, ledStatus ? HIGH : LOW);

    if(input.dir == 'S') {
      motorSpeed = 0;
    } else if (input.dir == 'F' || input.dir == 'B') {
      set_direction(input.dir == 'F' ? FORWARD_DIR : BACKWARD_DIR);
      servoPos += (input.dir == 'F' ? 1 : -1);
      motorSpeed = (input.val / INPUT_MOTOR_RATIO) + MIN_MOTOR_SPEED;
    }
    Serial.print("Motor Speed: "); Serial.println(motorSpeed);
    Serial.print("Direction: "); Serial.println(input.dir);

    inputDir = input.dir;
  }
  
  /*digitalWrite(dir1Pin, HIGH);
  digitalWrite(dir2Pin, LOW);
  potValue = analogRead(potPin);
  Serial.print("Pot value: "); Serial.println(potValue);

  if(motorSpeed == 0 && potValue > 0){
      analogWrite(speedPin, 255);
      delay(25);
  }
  if(potValue > 0){
      motorSpeed = int(potValue / POT_MOTOR_RATIO) + MIN_SPEED;
      Serial.println(potValue / POT_MOTOR_RATIO);
  }else{
      motorSpeed = 0;
  }*/

  // Serial.print("Speed: "); Serial.println(motorSpeed);
  if(motorSpeed > 0){
    //steppermotor.setSpeed(motorSpeed*2);
    //steppermotor.step(inputDir == 'F' ? 1 : -1);
  } else {
    //steppermotor.setSpeed(0);
  }
  if(motorSpeed > 255) motorSpeed = 255;
  if(inputDir != 'S') servoPos += (inputDir == 'F' ? 1 : -1);
  analogWrite(speedPin, motorSpeed);

  if(servoPos > 180) servoPos = 180;
  else if (servoPos < 0) servoPos = 0;
  myServo.write(servoPos);

  delay(15);
}
