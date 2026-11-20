#define BLYNK_TEMPLATE_ID "TMPL60dKhGIXs"
#define BLYNK_TEMPLATE_NAME "lab"
#define BLYNK_AUTH_TOKEN "_9QP7Vd-czynlEl_uMq872XeEIHbVSkt"
 
#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

// Gunakan huruf kapital untuk konstanta #define agar tidak bentrok dengan nama parameter fungsi
#define IN1 25
#define IN2 26
#define IN3 27
#define IN4 14

void Motor_init(int pin1, int pin2) {
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
}

// Perbaikan: Tambahkan tipe data 'int' pada parameter dan balik logika negatif/positif
void Motor_setSpeed(int speed, int pin1, int pin2) {
  // Batasi nilai speed agar tetap di rentang -255 sampai 255
  speed = constrain(speed, -255, 255);

  if (speed > 0) {
    analogWrite(pin1, speed);
    digitalWrite(pin2, LOW);
  } 
  else if (speed < 0) {
    digitalWrite(pin1, LOW);
    analogWrite(pin2, -speed); // Ubah negatif menjadi positif untuk nilai PWM
  } 
  else {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
  }
}

void Motor_stop(int pin1, int pin2) {
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
}

// Perbaikan: Ubah tipe fungsi ke 'void' karena tidak mengembalikan (return) nilai
void mechanum_speed(int vx, int vy, int omega) {
  float rawFL = vy + vx + omega;
  float rawFR = vy - vx - omega;
  float rawRL = vy - vx + omega;
  float rawRR = vy + vx - omega;

  float maxVal = max(abs(rawFL), max(abs(rawFR), max(abs(rawRL), abs(rawRR))));
  if (maxVal > 255) {
    rawFL = (rawFL / maxVal) * 255;
    rawFR = (rawFR / maxVal) * 255;
    rawRL = (rawRL / maxVal) * 255;
    rawRR = (rawRR / maxVal) * 255;
  }
}

void setup() {
  // Perbaikan: Sesuaikan huruf kapital 'M' pada Motor_init
  Motor_init(IN1, IN2);
  Motor_init(IN3, IN4);
  
  // Untuk ESP32, baud rate standar yang umum digunakan adalah 115200 (9600 juga tetap bisa)
  Serial.begin(115200); 
}

void loop() {
  // Perbaikan: Gunakan Serial.println() untuk mencetak teks, dan tambahkan titik koma (;)
  Serial.println("Motor: ON");
  Motor_setSpeed(255, IN1, IN2);
  Motor_setSpeed(255, IN3, IN4);
  delay(1000);

  Serial.println("Motor: OFF");
  Motor_stop(IN1, IN2);
  Motor_stop(IN3, IN4);
  delay(1000);
}
