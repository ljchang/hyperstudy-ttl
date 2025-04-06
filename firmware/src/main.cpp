#include <Adafruit_TinyUSB.h>

#define TRIGGER_PIN 5
#define PULSE_DURATION_MS 10

void setup() {
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW);

  TinyUSBDevice.setWebUSBLandingPage("https://yourusername.github.io/hyperstudy-ttl/web");

  Serial.begin(115200); // For debug only
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "pulse") {
      digitalWrite(TRIGGER_PIN, HIGH);
      delay(PULSE_DURATION_MS);
      digitalWrite(TRIGGER_PIN, LOW);
      Serial.println("✅ Pulse sent");
    }
  }
}
