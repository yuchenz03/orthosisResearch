//run this code in Arduino IDE to format data for one sensor reading

const int foamPin = A0; //Analog pin to read from
const float Vcc = 5.0; //Supply voltage
const float fixedR = 20000.0; //using 20k ohm resistor

void setup() {
  Serial.begin(9600); //baud rate: 9600
}

void loop() {
  int raw = analogRead(foamPin); //raw data input from arduino
  float Vout = raw * (Vcc / 1023.0); //converting arduino input into voltage

  foamR = fixedR * (Vout / (Vcc - Vout)); //calculating foam resistance

  Serial.println(foamR);  // Output only numeric value for Serial Plotter
  delay(50); //20 data points per second
}
