//run this code in Arduino IDE to format data for four sensors

const float Vcc = 5.0; //Supply voltage
const float fixedR = 20000.0; //using 20k ohm resistor

void setup() {
  Serial.begin(9600); //baud rate: 9600
}

void loop() {
  float values[4];

  for (int i = 0; i < 4; i++) {
    int raw = analogRead(i);  //A0–A3 are addressed as 0–3
    float Vout = raw * (Vcc / 1023.0);
    values[i] = fixedR * (Vout / (Vcc - Vout));
  }

  //printing data as 4 comma separated values
  for (int i = 0; i < 4; i++) {
    Serial.print(values[i]);
    if (i < 3) Serial.print(",");
    else Serial.println(); 
  }

  delay(50);
}