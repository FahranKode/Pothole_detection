#pragma once
#include <Arduino.h>

class Motor {
private:
    uint8_t in1, in2;

public:
    Motor(uint8_t in1, uint8_t in2) : in1(in1), in2(in2) {}

    void init();
    // void forward(uint8_t speed);
    // void backward(uint8_t speed);
    void stop();
    void drive(uint8_t speed);
};

class MechanumWheel {
private:
    Motor frontLeft;
    Motor frontRight;
    Motor backLeft;
    Motor backRight;

public:
    // Pass by const reference (&) lebih efisien daripada copy object
    MechanumWheel(const Motor& fl, const Motor& fr, const Motor& bl, const Motor& br)
        : frontLeft(fl), frontRight(fr), backLeft(bl), backRight(br) {}

    void init() {
        frontLeft.init();
        frontRight.init();
        backLeft.init();
        backRight.init();
    }

    void drive(int vx, int vy, int omega );

    // void moveForward(uint8_t speed);
    // void moveBackward(uint8_t speed);
    // void strafeLeft(uint8_t speed);
    // void strafeRight(uint8_t speed);
    // void rotateLeft(uint8_t speed);
    // void rotateRight(uint8_t speed);
    void stopAll();
};