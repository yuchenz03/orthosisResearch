const float Vcc = 5.0;
const float Vmid = Vcc / 2.0;

// ---- calibration table ----
const int NUM_POINTS = 19;
const int adcTable[NUM_POINTS] = {
    662, 660, 654, 642, 628, 610, 589, 563, 537,
    510,
    485, 455, 433, 408, 390, 374, 363, 357, 355};
const int angleTable[NUM_POINTS] = {
    -90, -80, -70, -60, -50, -40, -30, -20, -10,
    0,
    10, 20, 30, 40, 50, 60, 70, 80, 90};

float adcToAngle(int adc)
{
    if (adc >= adcTable[0])
        return angleTable[0];
    if (adc <= adcTable[NUM_POINTS - 1])
        return angleTable[NUM_POINTS - 1];
    for (int i = 0; i < NUM_POINTS - 1; i++)
    {
        int adcHigh = adcTable[i];
        int adcLow = adcTable[i + 1];
        if (adcHigh >= adc && adc >= adcLow)
        {
            float t = (float)(adc - adcLow) / (float)(adcHigh - adcLow);
            float angHigh = angleTable[i];
            float angLow = angleTable[i + 1];
            return angLow + t * (angHigh - angLow);
        }
    }
    return 0.0;
}

// --- new variables for angular velocity ---
float lastAngleDiff = 0.0;
unsigned long lastMicros = 0;

void setup()
{
    Serial.begin(9600);
    lastMicros = micros();
}

void loop()
{
    // read both sensors as before
    int rawX1 = analogRead(A4);
    int rawX2 = analogRead(A1);

    float angle1 = adcToAngle(rawX1);
    float angle2 = adcToAngle(rawX2);
    float angleDiff = angle2 - angle1;

    // --- compute time difference ---
    unsigned long nowMicros = micros();
    float dt = (nowMicros - lastMicros) / 1e6; // seconds
    if (dt <= 0)
        dt = 1e-3;

    // --- derivative (deg/s) ---
    float angularVel = (angleDiff - lastAngleDiff) / dt;

    // update stored values
    lastAngleDiff = angleDiff;
    lastMicros = nowMicros;

    // // --- print results ---
    // Serial.print("Angle1: "); Serial.print(angle1, 2);
    // Serial.print(", Angle2: "); Serial.print(angle1, 2);
    // Serial.print(", Diff: "); Serial.print(angleDiff, 2);
    // Serial.print(", dDiff/dt (deg/s): "); Serial.println(angularVel, 2);
    Serial.print(angle1, 2);
    Serial.print(", ");
    Serial.print(angle1, 2);
    Serial.print(", ");
    Serial.print(angleDiff, 2);
    Serial.print(", ");
    Serial.println(angularVel, 2);

    delay(100);
}
