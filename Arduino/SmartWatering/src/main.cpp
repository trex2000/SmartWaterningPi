#include <Arduino.h>
#include <TaskScheduler.h>

/*Pin numbers*/
const int ledPin1 = 5; //The number of the led 1 pin
const int ledPin2 = 4; //The number of the led 2 pin
const int buttonPin1 = 7; //The number if the push button 1 pin
const int buttonPin2 = 6; //The number of the push button 2 pin 

/*Values that are not constants*/
int buttonState1 = 1; //The initial value of the push button 1 state (HIGH/ push-up resistor)
int buttonState2 = 1; //The initial value of the push button 2 state

// Scheduler
Scheduler ts;

/*Task periods*/
#define PERIOD1 10
#define PERIOD2 20

/*The Callback function for the 10 ms task*/
void Tasks10ms(){
}

/*The Callback function for the 20 ms task*/
void Tasks20ms(){
}

/*The 10 and the 20 ms task*/
Task Task10ms ( PERIOD1 * TASK_MILLISECOND, TASK_FOREVER , &Tasks10ms, &ts, true );
Task Task20ms ( PERIOD2* TASK_MILLISECOND, TASK_FOREVER , &Tasks20ms, &ts, true );


void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);

}

void loop() {
  // put your main code here, to run repeatedly:

  //read the state of the push button
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);

  //check if the push button 1 is pressed. If the button state is HIGH
  if (buttonState1 == HIGH) {
    //turn LED 1 off
    digitalWrite(ledPin1, LOW);
  } else {
    //turn LED 1 on
    digitalWrite(ledPin1, HIGH);
  }
  
  //check if the push button 2 is pressed. If the button state is HIGH
  if (buttonState2 == HIGH) {
    //turn LED 2 off
    digitalWrite(ledPin2, LOW);
  } else {
    //turn LED 2 on
    digitalWrite(ledPin2, HIGH);
  }
  
  /*Start the task scheduler*/
  ts.execute();
}


