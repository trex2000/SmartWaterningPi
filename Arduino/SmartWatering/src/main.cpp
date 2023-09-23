#include <Arduino.h>
#include <TaskScheduler.h>


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

}

void loop() {
  // put your main code here, to run repeatedly:
  
  /*Start the task scheduler*/
  ts.execute();
}

