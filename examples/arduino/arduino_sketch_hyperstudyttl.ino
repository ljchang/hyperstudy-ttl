#include <Arduino.h>
#include <Adafruit_TinyUSB.h>

// Define constants for trigger pin and pulse duration
const int TRIGGER_PIN = 5;
const int PULSE_DURATION_MS = 10;

void setup()
{
    // Initialize the trigger pin
    pinMode(TRIGGER_PIN, OUTPUT);
    digitalWrite(TRIGGER_PIN, LOW);

    // Start serial communication (works for both WebUSB and CDC)
    Serial.begin(115200);
    while (!Serial)
    {
        delay(10);
    }
    Serial.println("🟢 RP2040 WebUSB Trigger Ready");
}

void loop()
{
    // Check if a command is available on the serial interface
    if (Serial.available() > 0)
    {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();

        // Check for the "pulse" command (case-insensitive)
        if (cmd.equalsIgnoreCase("pulse"))
        {
            Serial.println("⚡ Triggering TTL pulse!");
            digitalWrite(TRIGGER_PIN, HIGH);
            delay(PULSE_DURATION_MS);
            digitalWrite(TRIGGER_PIN, LOW);
            Serial.println("✅ Pulse sent");
        }
        else
        {
            Serial.println("❓ Unknown command: " + cmd);
        }
    }
    // Small delay to avoid busy looping
    delay(10);
}