
const int pins[6] = {2, 3, 4, 5, 6, 7}; // 6 pins for bitmask
const int toggle1Pin = 12;
const int toggle2Pin = 13;
const int radioA[2] = {8,9};
const int radioB[2] = {10,11};

void setup() {
  Serial.begin(9600);

  // Setup pins
  pinMode(toggle1Pin, OUTPUT);
  pinMode(toggle2Pin, OUTPUT);
  for (int i = 0; i <2; i++) pinMode(radioA[i], OUTPUT);
  for (int i = 0; i <2; i++) pinMode(radioB[i], OUTPUT);
  for (int i = 0; i < 6; i++) pinMode(pins[i], OUTPUT);

  Serial.println("Arduino ready to receive packets...");
}

void loop() {
   if (Serial.available() >= 2) {
    int component_id = Serial.parseInt();
    int value = Serial.parseInt();

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

      Serial.print("Radio Group A -> Option ");
      Serial.println(value);

    } else if (component_id == 5) {
      // Radio Group A
           for (int i = 0; i < 2; i++) {
        int bitVal = (value >> i) & 1;
        digitalWrite(radioB[i], bitVal);
      }

      Serial.print("Radio Group B -> Option ");
      Serial.println(value);

    }  else {
      Serial.print("Unknown Component ID: ");
      Serial.println(component_id);
    }
 }
}
