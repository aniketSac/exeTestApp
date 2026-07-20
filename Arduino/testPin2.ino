
const int pins[6] = {2, 3, 4, 5, 6, 7}; // 6 pins for bitmask
const int toggle1Pin = 0;
const int toggle2Pin = 1;
const int radioA[2] = {10,11};
// const int radioA1 = 10;
// const int radioA2 = 11;
//https://wokwi.com/projects/469524474082185217
//https://wokwi.com/projects/469526473197960193
void setup() {
  // Serial.begin(9600);

  // Setup pins
  for (int i = 0; i <2; i++) pinMode(radioA[i], OUTPUT);
  for (int i = 0; i < 6; i++) pinMode(pins[i], OUTPUT);
  pinMode(toggle1Pin, OUTPUT);
  pinMode(toggle2Pin, OUTPUT);
  // pinMode(radioA1, OUTPUT);
  // pinMode(radioA2, OUTPUT);

    // byte component_id = 1;
    // byte value = x02;

  Serial.println("Arduino ready to receive packets...");
}

void loop() {
  // if (Serial.available() >= 2) {
    byte component_id = 1;
    byte value = '&';

    if (component_id == 1) {
      // Bitmask update (6 pins)
      for (int i = 0; i < 6; i++) {
        int bitVal = (value >> i) & 1;
        digitalWrite(pins[i], bitVal);
      }
      Serial.print("Bitmask applied: ");
      Serial.println(value, BIN);

    } else if (component_id == 2) {
      digitalWrite(toggle1Pin, value == 1 ? HIGH : LOW);
      Serial.println(value == 1 ? "Toggle 1 ON" : "Toggle 1 OFF");

    } else if (component_id == 3) {
      digitalWrite(toggle2Pin, value == 1 ? HIGH : LOW);
      Serial.println(value == 1 ? "Toggle 2 ON" : "Toggle 2 OFF");

    } else if (component_id == 4) {
      // Radio Group A
           for (int i = 0; i < 2; i++) {
        int bitVal = (value >> i) & 1;
        digitalWrite(radioA[i], bitVal);
      }
      //   for (int j = 0; j < 2; j++) {
      //   int bitVal = (value >> i) & 1;
      // digitalWrite(radioA1, value == 0 ? HIGH : LOW);
      // digitalWrite(radioA2, value == 1 ? HIGH : LOW);
      // }
      Serial.print("Radio Group A -> Option ");
      Serial.println(value);

    }  else {
      Serial.print("Unknown Component ID: ");
      Serial.println(component_id);
    }
  // }
}
