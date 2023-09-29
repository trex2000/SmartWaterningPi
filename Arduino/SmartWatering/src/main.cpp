#include <Arduino.h>
#include <TaskScheduler.h>

/*The pin number of LED 1*/

/*The pin number of LED 2*/



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
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(5, HIGH);
  delay(1000);
  digitalWrite(4, HIGH);
  delay(1000);
  digitalWrite(5, LOW);
  delay(1000);
  digitalWrite(4, LOW);
  delay(1000);
  
  /*Start the task scheduler*/
  ts.execute();
}

