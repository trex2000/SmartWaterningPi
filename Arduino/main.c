//#define IO_DEBUG
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
Task Task20ms ( PERIOD1* TASK_MILLISECOND, TASK_FOREVER , &Tasks20ms, &ts, true );

void setup() {
  /*Initialize the  software components here*/

}

void loop() {

  /*Start the task scheduler*/
  ts.execute();
  
}
