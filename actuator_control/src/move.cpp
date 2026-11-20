// Helper untuk menggerakkan 1 motor berdasarkan nilai bertanda (-255 sampai 255)
void MechanumWheel::driveMotor(Motor& m, int speed) {
    if (speed > 15) { // Deadzone kecil agar motor tidak berdengung saat joystick diam
        m.forward(constrain(speed, 0, 255));
    } else if (speed < -15) {
        m.backward(constrain(abs(speed), 0, 255));
    } else {
        m.stop();
    }
}

void MechanumWheel::cal_velo(int vx, int vy, int omega) {
    // 1. Hitung kinematika mentah
    float rawFL = vy + vx + omega;
    float rawFR = vy - vx - omega;
    float rawRL = vy - vx + omega;
    float rawRR = vy + vx - omega;

    // 2. Cari nilai maksimum absolut
    float maxVal = max(max(abs(rawFL), abs(rawFR)), max(abs(rawRL), abs(rawRR)));

    // 3. Normalisasi ke rentang maksimal PWM (255)
    if (maxVal > 255.0) {
        rawFL = (rawFL / maxVal) * 255.0;
        rawFR = (rawFR / maxVal) * 255.0;
        rawRL = (rawRL / maxVal) * 255.0;
        rawRR = (rawRR / maxVal) * 255.0;
    }

    // 4. Eksekusi langsung ke masing-masing motor
    driveMotor(frontLeft,  (int)rawFL);
    driveMotor(frontRight, (int)rawFR);
    driveMotor(backLeft,   (int)rawRL);
    driveMotor(backRight,  (int)rawRR);
}