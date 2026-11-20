#include "omniwheel.hpp" // Pastikan sama dengan nama file header

void Motor::init() {
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    stop();
}

void Motor::drive(int16_t speed) {
    // Safety clamp agar tidak lewat batas PWM 8-bit
    speed = constrain(speed, -255, 255);

    if (speed > 0) {
        analogWrite(in1, speed);
        digitalWrite(in2, LOW);
    } else if (speed < 0) {
        digitalWrite(in1, LOW);
        analogWrite(in2, -speed);
    } else {
        stop(); // Eksplisit matikan kedua pin jika speed == 0
    }
}

void Motor::stop() {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
}

void MechanumWheel::stopAll() {
    frontLeft.stop();
    frontRight.stop();
    backLeft.stop();
    backRight.stop();
}

void MechanumWheel::drive(int vx, int vy, int omega) {
    float rawFL = vy + vx + omega;
    float rawFR = vy - vx - omega;
    float rawRL = vy - vx + omega;
    float rawRR = vy + vx - omega;

    // Gunakan fabs() untuk float dan simpan di float
    float maxVal = max(fabs(rawFL), max(fabs(rawFR), max(fabs(rawRL), fabs(rawRR))));

    if (maxVal > 255.0f) {
        rawFL = (rawFL / maxVal) * 255.0f;
        rawFR = (rawFR / maxVal) * 255.0f;
        rawRL = (rawRL / maxVal) * 255.0f;
        rawRR = (rawRR / maxVal) * 255.0f;
    }

    frontLeft.drive((int16_t)rawFL);
    frontRight.drive((int16_t)rawFR);
    backLeft.drive((int16_t)rawRL);
    backRight.drive((int16_t)rawRR);
}