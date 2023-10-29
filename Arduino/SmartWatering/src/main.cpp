#include <Arduino.h>
#include <TaskScheduler.h>

/*Pin numbers*/
#define LED_PIN_1 5 //The number of the led 1 pin
#define LED_PIN_2 4 //The number of the led 2 pin
#define BUTTON_PIN_1 7 //The number if the push button 1 pin
#define BUTTON_PIN_2 6 //The number of the push button 2 pin 

/*Values that are not constants*/
int buttonState1 = HIGH; //The initial value of the push button 1 state (HIGH/ push-up resistor)
int buttonState2 = HIGH; //The initial value of the push button 2 state
bool ledState1 = false;
bool ledState2 = false;

unsigned int T_BOUNCE_INIT_VALUE = 50; // debounce counter's initial value
unsigned int T_SLEEP = 0.01; // sleep time
unsigned int CNT_ELAPSED_VALUE = 0; // counter is running and reached 0
unsigned int CNT_STOPPED_VALUE = 0xFFFF; // counter was stopped and is not running 
unsigned int debounce_counter1 = T_BOUNCE_INIT_VALUE;
unsigned int debounce_counter2 = T_BOUNCE_INIT_VALUE;

/*Function declarations*/
bool counter_is_running(int counter);
int counter_elapsed(int counter);
int start_counter(int counter, int initial_value);
int stop_counter(int counter);

// Scheduler
Scheduler ts;

/*Task periods*/
#define PERIOD1 10
#define PERIOD2 20


/*The Callback function for the 10 ms task*/
void led_1_blink(){

  //read the state of the push button 1
  buttonState1 = digitalRead(BUTTON_PIN_1);

  if (buttonState1 == LOW){
    if (counter_is_running(debounce_counter1)){
      debounce_counter1 = debounce_counter1 - 1;
    } else if (counter_elapsed(debounce_counter1)){
      debounce_counter1 = stop_counter(debounce_counter1);
      if (ledState1 == false){
        digitalWrite(LED_PIN_1, HIGH);
        ledState1 = true;
      }else {
        digitalWrite(LED_PIN_1, LOW);
        ledState1 = false;
      }
    } else {
      debounce_counter1 = start_counter(debounce_counter1, T_BOUNCE_INIT_VALUE);
    }   
  }
}

/*The Callback function for the 20 ms task*/
void led_2_blink(){
  
  //read the state of the push button 2
  buttonState2 = digitalRead(BUTTON_PIN_2);

  if (buttonState2 == LOW){
    if (counter_is_running(debounce_counter2)){
      debounce_counter2 = debounce_counter2 - 1;
    } else if (counter_elapsed(debounce_counter2)){
      debounce_counter2 = stop_counter(debounce_counter2);
      if (ledState2 == false){
        digitalWrite(LED_PIN_2, HIGH);
        ledState2 = true;
      } else {
        digitalWrite(LED_PIN_2, LOW);
        ledState2 = false;
      }
    } else {
      debounce_counter2 = start_counter(debounce_counter2, T_BOUNCE_INIT_VALUE);
    }
  }
}

/*The 10 and the 20 ms task*/
Task Task10ms ( PERIOD1 * TASK_MILLISECOND, TASK_FOREVER , &led_1_blink, &ts, true );
Task Task20ms ( PERIOD2* TASK_MILLISECOND, TASK_FOREVER , &led_2_blink, &ts, true );


void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(BUTTON_PIN_1, INPUT_PULLUP);
  pinMode(BUTTON_PIN_2, INPUT_PULLUP);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  /*Start the task scheduler*/
  ts.execute();
}


/*Function definition*/

bool counter_is_running(int counter){
  if ((counter != CNT_ELAPSED_VALUE) and (counter != CNT_STOPPED_VALUE)){
    return true;
  } else {
    return false;
  }
}

int counter_elapsed(int counter){
    return (counter == CNT_ELAPSED_VALUE);
}

int start_counter(int counter, int initial_value){
  counter = initial_value;
  return counter;
}

int stop_counter(int counter){
  counter = CNT_STOPPED_VALUE;
  return counter;
}

