
#include <Arduino.h>
#include <DRV8825.h>

#include <ESP8266WebServer.h>
#include <ESP8266HTTPUpdateServer.h>

#include <ESP8266WiFi.h>

IPAddress local_IP(10, 0, 3, 99);
IPAddress gateway(10, 0, 3, 1);
IPAddress subnet(255, 255, 255, 0);

//const char* ssid = "RotaMixer";
//const char* password = "RotaMixer";



#define YOUR_WIFI_SSID "Pipettier"
#define YOUR_WIFI_PASSWD "Pipettier"

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200

#define DIR 16
#define STEP 14
#define ENABLE 13
#define MODE 12

#define MOTOR 4

#define START_SHAKER "0"
#define START_VAC "2"
#define STOP_SHAKER "1"
#define STOP_VAC "3"

DRV8825 stepper(MOTOR_STEPS, DIR, STEP, ENABLE, MODE, MODE, MODE);

String myVersion = "11052019_0";

int Mixer_stat= 0;
int Vac_stat = 0;
int power = 1023;

short rpm = 250;
long angle = 450000LL;
short micro = 32;
short accel = 1500;
short decel = 1500;

ESP8266WebServer httpServer(80);
ESP8266HTTPUpdateServer httpUpdater(true);

uint32_t mics_1=0;
int64_t remain = 0;
int duration = 0 ;


void setup() {

    Serial.begin (115200);
    Serial.println ();

    Serial.print("Setting soft-AP configuration ... ");
    
    WiFi.mode (WIFI_STA);
    WiFi.begin (YOUR_WIFI_SSID, YOUR_WIFI_PASSWD);
    WiFi.config(local_IP,gateway,subnet);
    

    pinMode(MOTOR , OUTPUT);
    analogWrite(MOTOR , 0 );


     Serial.print("Connecting");
       while (WiFi.status() != WL_CONNECTED)
      {
         delay(500);
         Serial.print(".");
      }
      Serial.println();

       Serial.print("Connected, IP address: ");
      Serial.println(WiFi.localIP());
    

    
   httpServer.on("/", [](){

    if (httpServer.hasArg("action")) {
        if ( httpServer.arg("action")== START_SHAKER ){
              if ( Mixer_stat == 1 ){
                httpServer.send(200, "text/html","Shaker already started");  
                return;
              }
              rpm = httpServer.arg("rpm").toInt();
              if (httpServer.arg("time" )!= "") {
                duration = httpServer.arg("time").toInt();

                angle = int(rpm/60*360 * duration);
              } else {
                angle = httpServer.arg("angle").toInt();
                duration = int( angle/rpm * 60/360);
              }
              remain = (int64_t )duration *  1000LL * 1000LL;
              stepper.setRPM(rpm);
              mics_1 = micros();
              
              stepper.enable();
              Mixer_stat = 1;
              httpServer.send(200, "text/html","Shaker started"); 
        }else if ( httpServer.arg("action")== STOP_SHAKER ){
              if ( Mixer_stat == 0 ){
                httpServer.send(200, "text/html","Shaker not running");  
                return;
              }
              remain = 0 ;
              httpServer.send(200, "text/html","Shaker stopped");
        }else if ( httpServer.arg("action")== START_VAC ){
              if (Mixer_stat == 1 ) {
                  Mixer_stat = 0;
                  remain = 0;
                  stepper.stop();
                  stepper.disable();
              }
              duration = httpServer.arg("time").toInt();
              power = httpServer.arg("power").toInt();
              mics_1 = micros();
              remain = (int64_t )duration *  1000LL * 1000LL;
              Vac_stat = 1;
              httpServer.send(200, "text/html","Vac_Pump started");
              analogWrite(MOTOR, power);              
        }else if ( httpServer.arg("action")== STOP_VAC ){
              remain = 0;
              httpServer.send(200, "text/html","Vac_Pump stopped");             
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
    stepper.begin(rpm,micro);
    stepper.setSpeedProfile(stepper.LINEAR_SPEED, accel,decel);
    stepper.disable();


   
}

void loop() {

     httpServer.handleClient();


     if (Mixer_stat == 1) {
      
          Serial.printf ("Mixer loop \r\n");
          stepper.startRotate(angle);     // forward revolution
          
          while (stepper.nextAction() ) {
              httpServer.handleClient(); 
              
              if (remain > 0 ) {
                        uint32_t mics_2 = micros();
                        uint32_t diff =  mics_2 -  mics_1;
                        remain = remain-diff;
                        mics_1 = mics_2;                       
               } 
               //else stepper.startBrake();
                
          }
          Mixer_stat = 0;
          stepper.disable();
     }

     if (Vac_stat == 1) {
          while (remain > 0) {
                 delay(100);
                 httpServer.handleClient(); 
                 uint32_t mics_2 = micros();
                 uint32_t diff =  mics_2 -  mics_1;
                 remain = remain-diff;
                 mics_1 = mics_2; 
          }
          analogWrite(MOTOR, 0); 
          Vac_stat = 0;
         
     }

}
