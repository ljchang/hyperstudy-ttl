#include <Arduino.h>
#include <Adafruit_TinyUSB.h>
#include <pico/unique_id.h>

// Configuration
#define TRIGGER_PIN 6  // D4 pin on Feather RP2040 = GP06
#define DEFAULT_PULSE_DURATION_MS 10
#define MAX_PULSE_DURATION_MS 10000

// Firmware version for device identification
#define FIRMWARE_VERSION "1.4.0"

// Board unique serial number (populated from flash chip ID in setup)
static char board_serial[2 * PICO_UNIQUE_BOARD_ID_SIZE_BYTES + 1];

// Configurable default pulse duration (settable via SETDURATION command)
static int pulse_duration_ms = DEFAULT_PULSE_DURATION_MS;

// Last pulse timing (microseconds from serial-available to GPIO toggle)
static unsigned long last_pulse_timing_us = 0;

void setup() {
  // Read unique board ID from flash chip (each RP2040 board has a unique ID)
  pico_get_unique_board_id_string(board_serial, sizeof(board_serial));

  // Initialize trigger pin for OFF-to-ON pulse behavior
  // HCPL-2211 has totem pole output (non-inverting, no pull-up needed):
  // GPIO LOW -> LED OFF -> Output LOW (idle state)
  // GPIO HIGH -> LED ON -> Output HIGH (pulse active)
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW);  // Start with LED OFF (output LOW/idle)

  // Initialize USB Serial (compatible with hyperstudy-bridge)
  // USB serial descriptor is auto-generated from flash unique ID by TinyUSB
  Serial.begin(115200);

  // Wait briefly for USB connection
  while (!Serial && millis() < 5000) {
    delay(10);
  }

  Serial.println("RP2040 TTL Trigger Ready");
  Serial.print("Firmware Version: ");
  Serial.println(FIRMWARE_VERSION);
  Serial.print("Serial: ");
  Serial.println(board_serial);
  Serial.print("Trigger Pin: GP");
  Serial.println(TRIGGER_PIN);
  Serial.print("Default Pulse Duration: ");
  Serial.print(DEFAULT_PULSE_DURATION_MS);
  Serial.println("ms");
  Serial.println("Commands: PULSE [ms], SETDURATION <ms>, TIMING, TEST, VERSION, SERIAL");
}

void loop() {
  if (Serial.available() > 0) {
    unsigned long t_available = micros();
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();  // Accept case-insensitive commands

    if (cmd == "PULSE" || cmd.startsWith("PULSE ")) {
      // CRITICAL PATH: Toggle GPIO as fast as possible
      digitalWrite(TRIGGER_PIN, HIGH);
      last_pulse_timing_us = micros() - t_available;

      // Parse optional inline duration AFTER GPIO is already HIGH (not latency-critical)
      int duration = pulse_duration_ms;
      if (cmd.length() > 6) {
        int parsed = cmd.substring(6).toInt();
        if (parsed > 0 && parsed <= MAX_PULSE_DURATION_MS) {
          duration = parsed;
        }
      }

      delay(duration);
      digitalWrite(TRIGGER_PIN, LOW);  // Return to idle (output LOW)

      Serial.println("OK:Pulse sent");

    } else if (cmd.startsWith("SETDURATION ")) {
      // Configure default pulse duration (used when PULSE has no inline parameter)
      int parsed = cmd.substring(12).toInt();
      if (parsed > 0 && parsed <= MAX_PULSE_DURATION_MS) {
        pulse_duration_ms = parsed;
        Serial.print("OK:Duration set to ");
        Serial.print(pulse_duration_ms);
        Serial.println("ms");
      } else {
        Serial.print("ERROR:Invalid duration. Range: 1-");
        Serial.print(MAX_PULSE_DURATION_MS);
        Serial.println("ms");
      }

    } else if (cmd == "TIMING") {
      // Report last pulse timing (microseconds from serial-available to GPIO toggle)
      Serial.print("OK:Timing us:");
      Serial.print(last_pulse_timing_us);
      Serial.print(",dur:");
      Serial.println(pulse_duration_ms);

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

    } else if (cmd == "SERIAL") {
      // Report unique board serial number
      Serial.print("OK:Serial ");
      Serial.println(board_serial);

    } else if (cmd != "") {
      Serial.print("ERROR:Unknown command: ");
      Serial.println(cmd);
    }
  }
  // No delay — tight polling for minimum latency.
  // RP2040 is a dedicated device with nothing else to do.
  // USB serial buffer is filled by interrupts regardless of loop timing.
}
