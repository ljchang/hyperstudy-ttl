#include <Arduino.h>
#include <Adafruit_TinyUSB.h>

#define TRIGGER_PIN 5
#define PULSE_DURATION_MS 10

void setup() {
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, HIGH);  // HIGH = TTL output LOW (inverted by optocoupler)
  
  // Initialize USB Serial
  Serial.begin(115200);
  
  // Wait for USB connection (optional, remove for standalone operation)
  while (!Serial && millis() < 5000) {
    delay(10);
  }
  
  Serial.println("RP2040 TTL Trigger Ready");
  Serial.println("Send 'pulse' to trigger TTL pulse");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd == "pulse" || cmd == "PULSE") {
      Serial.println("Triggering pulse...");
      digitalWrite(TRIGGER_PIN, LOW);   // LOW = TTL output HIGH (inverted)
      delay(PULSE_DURATION_MS);
      digitalWrite(TRIGGER_PIN, HIGH);  // HIGH = TTL output LOW (inverted)
      Serial.println("OK:Pulse sent");
    } else if (cmd == "test") {
      Serial.println("OK:Test successful");
    } else if (cmd != "") {
      Serial.print("Unknown command: ");
      Serial.println(cmd);
    }
  }
  
  // Small delay to prevent CPU hogging
  delay(1);
}