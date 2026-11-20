// 1. Macro Blynk WAJIB paling atas sebelum include library-nya
#define BLYNK_TEMPLATE_ID "TMPL60pMQMEVY"
#define BLYNK_TEMPLATE_NAME "Cartenz"
#define BLYNK_AUTH_TOKEN "GANTI_DENGAN_TOKEN_BARU"
#define BLYNK_PRINT Serial

#include <Arduino.h> // 'A' kapital
#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include "omniwheel.hpp" // Pastikan sama dengan nama file asli

char ssid[] = "NAMA_WIFI";
char pass[] = "PASSWORD_WIFI";

Motor fl(25, 26);
Motor fr(27, 14);
Motor bl(32, 33);
Motor br(18, 19);
MechanumWheel robot(fl, fr, bl, br);

void setup() {
    Serial.begin(115200);
    robot.init();
    Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
}

void loop() {
    Blynk.run();
    // Nanti variabel vx, vy, omega diisi dari callback BLYNK_WRITE(V...)
    robot.drive(0, 0, 0); 
}