#include <Arduino.h>
#include <DRV8825.h>
#include <MultiDriver.h>
//#include <SyncDriver.h>

#include <ESP8266WebServer.h>
#include <ESP8266HTTPUpdateServer.h>

#include <ESP8266WiFi.h>

IPAddress local_IP(10, 0, 3, 1);
IPAddress gateway(10, 0, 3, 1);
IPAddress subnet(255, 255, 255, 0);

const char* ssid = "Pipettier";
const char* password = "Pipettier";   // min 8 chars

#define STARTED 0
#define INITIALIZED 1

#define INIT "0"
#define RESET "5"
#define MOVE_X "6"
#define MOVE_Y "7"
#define MOVE_Z "8"
#define MOVE_PIP "9"
#define MOVE_XY "10"
#define SET_POS "11"


// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200

#define DIR_X 4
#define STEP_X 5
#define DIR_Y 1 
#define STEP_Y 3
#define DIR_Z 14
#define STEP_Z 16
#define DIR_PIP 12
#define STEP_PIP 13
#define ENABLE 15
#define MODE 2


DRV8825 stepper_x(MOTOR_STEPS, DIR_X, STEP_X, ENABLE, MODE, MODE, MODE);
DRV8825 stepper_y(MOTOR_STEPS, DIR_Y, STEP_Y, ENABLE, MODE, MODE, MODE);
DRV8825 stepper_z(MOTOR_STEPS, DIR_Z, STEP_Z, ENABLE, MODE, MODE, MODE);
DRV8825 stepper_pip(MOTOR_STEPS, DIR_PIP, STEP_PIP, ENABLE, MODE, MODE, MODE);
MultiDriver controller(stepper_x, stepper_y);

String myVersion = "11052019_0";

int pip_stat= STARTED;

short accel = 1500;
short decel = 1500;
signed long position[4];

ESP8266WebServer httpServer(80);
ESP8266HTTPUpdateServer httpUpdater(true);


void setup() {

//********** CHANGE PIN FUNCTION  TO GPIO **********
//GPIO 1 (TX) swap the pin to a GPIO.
    pinMode(1, FUNCTION_3); 
//GPIO 3 (RX) swap the pin to a GPIO.
    pinMode(3, FUNCTION_3); 
//**************************************************
    pinMode(DIR_X, OUTPUT);
    digitalWrite(DIR_X,LOW);
    pinMode(STEP_X, OUTPUT);
    digitalWrite(STEP_X,LOW);
    pinMode(DIR_Y, OUTPUT);
    digitalWrite(DIR_Y,LOW);
    pinMode(STEP_Y, OUTPUT);
    digitalWrite(STEP_Y,LOW);
    pinMode(DIR_Z, OUTPUT);
    digitalWrite(DIR_Z,LOW);
    pinMode(STEP_Z, OUTPUT);
    digitalWrite(STEP_Z,LOW);
    pinMode(DIR_PIP, OUTPUT);
    digitalWrite(DIR_PIP,LOW);
    pinMode(STEP_PIP, OUTPUT);
    digitalWrite(STEP_PIP,LOW);
    pinMode(ENABLE, OUTPUT);
    digitalWrite(ENABLE,LOW);
    pinMode(MODE, OUTPUT);
    digitalWrite(MODE,HIGH);
    Serial.begin (115200);
    Serial.println ();

    Serial.print("Setting soft-AP configuration ... ");
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(local_IP, gateway, subnet);
    WiFi.softAP(ssid, password);

     httpServer.on("/", [](){

    if (httpServer.hasArg("action")) {
        if (httpServer.arg("action")== INIT && pip_stat== STARTED)  {
            position[0]=position[1]=position[2]=position[3]=0;
            stepper_x.setRPM(httpServer.arg("x").toInt());
            stepper_y.setRPM(httpServer.arg("y").toInt());
            stepper_z.setRPM(httpServer.arg("z").toInt());
            position[3] = httpServer.arg("pip").toInt();
            position[2] = httpServer.arg("z_0").toInt();
            stepper_pip.enable();
            controller.enable();
            stepper_z.enable();
            stepper_pip.move(position[3]);   
            pip_stat = INITIALIZED;     
            httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));  
        } else if ( httpServer.arg("action")== RESET && pip_stat== INITIALIZED ){
              position[0]=position[1]=position[2]=position[3]=0;
              controller.disable();
              stepper_z.disable();
              stepper_pip.disable();
              pip_stat = STARTED;
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(STARTED));
        }else if ( httpServer.arg("action")== SET_POS && pip_stat== INITIALIZED ){
              position[0]= httpServer.arg("x").toInt();
              position[1]=httpServer.arg("y").toInt();
              position[2]=httpServer.arg("z").toInt();
              position[3]=httpServer.arg("pip").toInt();;
              pip_stat = INITIALIZED;
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));
        }else if ( httpServer.arg("action")== MOVE_XY && pip_stat== INITIALIZED ){
              long pos_x = httpServer.arg("x").toInt();
              long pos_y = httpServer.arg("y").toInt();
              signed long steps_x = pos_x - position[0] ;
              signed long steps_y = pos_y - position[1];
              stepper_x.setRPM(httpServer.arg("rpm").toInt());
              stepper_y.setRPM(httpServer.arg("rpm").toInt());
              position[0] = pos_x ;
              position[1] = pos_y;
              controller.move(steps_x,steps_y);
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));
        }else if ( httpServer.arg("action")== MOVE_X && pip_stat== INITIALIZED ){
              long pos_x = httpServer.arg("x").toInt();
              signed long steps_x = pos_x - position[0];
              stepper_x.setRPM(httpServer.arg("rpm").toInt());
              position[0] = pos_x ;
              stepper_x.move(steps_x);
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));
        }else if ( httpServer.arg("action")== MOVE_Y && pip_stat== INITIALIZED ){
              long pos_y = httpServer.arg("y").toInt();
              signed long steps_y = pos_y - position[1];
              stepper_y.setRPM(httpServer.arg("rpm").toInt());
              position[1] = pos_y;
              stepper_y.move(steps_y);
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));
        }else if ( httpServer.arg("action")== MOVE_Z && pip_stat== INITIALIZED ){
              long pos_z = httpServer.arg("z").toInt();
              signed long steps_z = pos_z - position[2];
              stepper_z.setRPM(httpServer.arg("rpm").toInt());
              position[2] = pos_z;
              stepper_z.move(steps_z);
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));
        }else if ( httpServer.arg("action")== MOVE_PIP && pip_stat== INITIALIZED ){
              long pos_pip = httpServer.arg("pip").toInt();
              signed long steps_pip = pos_pip - position[3];
              stepper_pip.setRPM(httpServer.arg("rpm").toInt());
              position[3] = pos_pip;
              stepper_pip.move(steps_pip);
              httpServer.send(200, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";"+String(INITIALIZED));
        } else {
          httpServer.send(300, "text/html",String(position[0])+";"+ String(position[1])+";"+ String(position[2])+";"+ String(position[3])+";Wrong state");
        }
    }    

    });

  
   httpServer.on("/version", [](){
    httpServer.send(200, "text/plain", "Installed Version: " + myVersion);
   });

  
  httpUpdater.setup(&httpServer);
  httpServer.begin();
        /*
     * Set target motor RPM.
     */
    stepper_pip.begin(10,32);
    stepper_pip.setSpeedProfile(stepper_pip.LINEAR_SPEED, accel,decel);
    stepper_pip.disable();

    stepper_y.begin(10,32);
    stepper_y.setSpeedProfile(stepper_y.LINEAR_SPEED, accel,decel);
    stepper_y.disable();
    
    stepper_x.begin(10,32);
    stepper_x.setSpeedProfile(stepper_x.LINEAR_SPEED, accel,decel);
    stepper_x.disable();

    stepper_z.begin(10,32);
    stepper_z.setSpeedProfile(stepper_z.LINEAR_SPEED, accel,decel);
    stepper_z.disable();

       
}

void loop() {

     httpServer.handleClient();
  
}
