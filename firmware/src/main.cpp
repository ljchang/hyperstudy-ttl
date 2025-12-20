#include <Arduino.h>
#include <Adafruit_TinyUSB.h>

// Configuration
#define TRIGGER_PIN 6  // D4 pin on Feather RP2040 = GP06
#define PULSE_DURATION_MS 10

// Firmware version for device identification
#define FIRMWARE_VERSION "1.3.0"

void setup() {
  // Initialize trigger pin for OFF-to-ON pulse behavior
  // HCPL-2211 has totem pole output (non-inverting, no pull-up needed):
  // GPIO LOW -> LED OFF -> Output LOW (idle state)
  // GPIO HIGH -> LED ON -> Output HIGH (pulse active)
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW);  // Start with LED OFF (output LOW/idle)

  // Initialize USB Serial (compatible with hyperstudy-bridge)
  Serial.begin(115200);

  // Wait briefly for USB connection
  while (!Serial && millis() < 5000) {
    delay(10);
  }

  Serial.println("RP2040 TTL Trigger Ready");
  Serial.print("Firmware Version: ");
  Serial.println(FIRMWARE_VERSION);
  Serial.print("Trigger Pin: GP");
  Serial.println(TRIGGER_PIN);
  Serial.println("Send 'PULSE' to trigger TTL pulse");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();  // Accept case-insensitive commands

    if (cmd == "PULSE") {
      // Send TTL pulse: GPIO HIGH = LED ON = output HIGH (active)
      digitalWrite(TRIGGER_PIN, HIGH);
      delay(PULSE_DURATION_MS);
      digitalWrite(TRIGGER_PIN, LOW);  // Return to idle (output LOW)

      // Response format compatible with hyperstudy-bridge
      Serial.println("OK:Pulse sent");

    } else if (cmd == "LONGPULSE") {
      // Long pulse for testing/visibility (3 seconds)
      digitalWrite(TRIGGER_PIN, HIGH);
      delay(3000);
      digitalWrite(TRIGGER_PIN, LOW);  // Return to idle (output LOW)
      Serial.println("OK:Long pulse sent");

    } else if (cmd == "TEST") {
      // Test command for connection validation
      Serial.println("OK:Test successful");

    } else if (cmd == "VERSION") {
      // Version query for device identification
      Serial.print("OK:Version ");
      Serial.println(FIRMWARE_VERSION);

    } else if (cmd != "") {
      Serial.print("ERROR:Unknown command: ");
      Serial.println(cmd);
    }
  }

  // Small delay to prevent CPU hogging
  delay(1);
}
