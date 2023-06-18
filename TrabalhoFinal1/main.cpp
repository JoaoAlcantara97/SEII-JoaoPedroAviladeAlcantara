#include <Arduino.h>

#define LED 2

#define POT 32

#define motorPWM 26
#define motorIN1 33
#define motorIN2 25
#define Kp 200
#define Ki 0.001
#define Kd 90
#define Ta 1

#define target 8

const int numSamples = 50; // Number of samples to filteredInclination
double samples[numSamples];  // Array to store the samples
int currentIndex = 0;     // Current index in the array

double sensorMax = 2665.5;
double sensorMin = 1665.5;
double sensor = 0;
double angle = 0;
double speed = 0;

double error = 0;
double lasterror = 0;

double P = 0;
double Integral = 0;
double D = 0;

double readFilteredSensor(){
    // Read the sensor value or any input data
  double sensorValue = analogRead(POT);

  // Update the samples array
  samples[currentIndex] = sensorValue;
  currentIndex = (currentIndex + 1) % numSamples; // Circular buffer

  // Calculate the filteredInclination
  double filteredInclination = 0;
  for (int i = 0; i < numSamples; i++) {
    filteredInclination += samples[i];
  }
  filteredInclination /= numSamples;
  return filteredInclination;

}

void setupFilter(){
  for(int i = 0; i < numSamples; i++){
    samples[i] = 0.0;
  }
}



void printSensor(){
  Serial.print("angleVal: ");
  Serial.print(angle);
  Serial.print(" sensorMin: ");
  Serial.print(sensorMin);
  Serial.print(" sensorMax: ");
  Serial.print(sensorMax);
  Serial.print(" sensorVal: ");
  Serial.print(sensor);
  Serial.print(" speed: ");
  Serial.print(speed);
  Serial.print(" error: ");
  Serial.print(error);
  Serial.print(" I: ");
  Serial.print(Integral);
  Serial.println();
  Serial.println();
}

void moveMotor(int speed){
  if(speed>=0){
    digitalWrite(motorIN1, HIGH);
    digitalWrite(motorIN2, LOW);
    analogWrite(motorPWM, speed);
  }
  else if(speed<0){
    digitalWrite(motorIN1, LOW);
    digitalWrite(motorIN2, HIGH);
    analogWrite(motorPWM, -speed);
  }

}

float mapf(float x, float in_min, float in_max, float out_min, float out_max) {
     float result;
     result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
     return result;
}

void setup(){
  Serial.begin(115200);

  pinMode(POT, INPUT);
  pinMode(motorIN1,OUTPUT);
  pinMode(motorIN2,OUTPUT);
  pinMode(motorPWM,OUTPUT);


  Serial.println("---Reading initial values, please wait.---");
  setupFilter();
  for (int i = 0; i<100; i++){
    readFilteredSensor();
  }

}


void loop(){

  unsigned long now = millis();
  sensor = readFilteredSensor();
  // if(sensor>sensorMax) sensorMax = sensor;
  // if(sensor<sensorMin) sensorMin = sensor;


  // Output the sensor
  
  angle = mapf(sensor, sensorMin, sensorMax, -45, 45);
  error = target - angle;
  printSensor();
  
  P = Kp*error;
  Integral = Integral + Ki*(error);
  D = Kd*(error-lasterror);

  lasterror = error;

  speed = P+Integral+D;
  speed = constrain(speed, -255, 255);
  moveMotor(speed);
  //Serial.println(-speed);

  while(millis() - now < Ta){
    
  }


  
  
}

