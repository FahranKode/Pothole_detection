#include<arduino.h>
#include "omni_wheel.hpp"

#define BLYNK_TEMPLATE_ID "TMPL60pMQMEVY"
#define BLYNK_TEMPLATE_NAME "Cartenz"
#define BLYNK_AUTH_TOKEN "8baBgItVXzRzXovZ7m9VEvNJuMrmTlkO"
#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

#define BLYNK_TEMPLATE_ID "TMPL60pMQMEVY"
#define BLYNK_TEMPLATE_NAME "Cartenz"
#define BLYNK_AUTH_TOKEN "8baBgItVXzRzXovZ7m9VEvNJuMrmTlkO"

#define BLYNK_PRINT Serial

Motor fl(25,26);
Motor fr(27,14);
Motor bl(32,33);
Motor br(18,19);
MechanumWheel robot(fl,fr,bl,br);

void setup(){
robot.init();

}
void loop(){

}