# HyperStudy TTL Installation Guide

Complete setup guide for the RP2040 TTL trigger device used with HyperStudy experiments.

## Architecture Overview

```
HyperStudy TriggerComponent → hyperstudy-bridge → RP2040 (this device) → TTL Output
```

**Data Flow:**
1. **TriggerComponent** (in HyperStudy experiment) sends trigger request
2. **hyperstudy-bridge** receives request via WebSocket and forwards to RP2040 via USB serial
3. **RP2040** (this firmware) sends TTL pulse on GPIO Pin 6 (D4) with configurable duration (default 10ms)
4. **Optocoupler** (HCPL-2211) provides electrical isolation to external equipment

## Hardware Requirements

- **Adafruit Feather RP2040** microcontroller
- **HCPL-2211** optocoupler (for electrical isolation)
- **330Ω resistor** (for LED current limiting)
- **0.1 µF capacitor** (decoupling)
- Breadboard and jumper wires
- BNC cable (for TTL output)
- USB-C cable

## Part 1: Hardware Assembly

### Wiring the Optocoupler

See [OPTOCOUPLER_WIRING.md](./OPTOCOUPLER_WIRING.md) for detailed wiring instructions.

**Quick Reference:**
```
Feather GPIO Pin 5 → 330Ω resistor → HCPL-2211 Pin 2 (Anode)
HCPL-2211 Pin 3 (Cathode) → Feather GND
HCPL-2211 Pin 8 (Vcc) → 5V (from Feather USB pin)
HCPL-2211 Pin 5 (GND) → Isolated GND rail (separate from Feather GND!)
HCPL-2211 Pin 6 (Output) → BNC center pin
BNC shield → Isolated GND rail
```

**Critical:** Input and output grounds must be separate for electrical isolation!

### Signal Behavior

- **Idle state:** GPIO Pin 5 = LOW (0V) → TTL Output = LOW
- **Pulse active:** GPIO Pin 5 = HIGH (3.3V) → TTL Output = HIGH (5V after optocoupler)
- **Pulse duration:** 10 milliseconds (configurable in firmware)

## Part 2: Firmware Installation

### Prerequisites

Install PlatformIO:
- **VS Code:** Install PlatformIO IDE extension
- **Command line:** `pip install platformio`

### Flash the Firmware

1. **Connect the Feather RP2040** to your computer via USB-C

2. **Navigate to firmware directory:**
   ```bash
   cd firmware
   ```

3. **Build and upload:**
   ```bash
   pio run --target upload
   ```

4. **Verify installation:**
   The device should appear as a USB serial port and display:
   ```
   RP2040 TTL Trigger Ready
   Firmware Version: 1.4.0
   Serial: <unique hex ID>
   Trigger Pin: GP6
   Default Pulse Duration: 10ms
   Commands: PULSE [ms], SETDURATION <ms>, TIMING, TEST, VERSION, SERIAL
   ```

### Test the Firmware

Open a serial monitor to test:

```bash
pio device monitor
```

**Test commands:**
- `PULSE` or `pulse` → Triggers TTL pulse (default 10ms), responds with `OK:Pulse sent`
- `PULSE 5` → Triggers 5ms TTL pulse, responds with `OK:Pulse sent`
- `SETDURATION 20` → Sets default pulse duration to 20ms
- `TIMING` → Reports last pulse timing (serial-to-GPIO latency in µs)
- `TEST` or `test` → Connection test, responds with `OK:Test successful`
- `VERSION` → Returns firmware version, responds with `OK:Version 1.4.0`
- `SERIAL` → Reports unique board serial number

**Expected behavior:** GPIO Pin 6 (D4) LED should flash briefly when you send `PULSE`.

## Part 3: Integration with hyperstudy-bridge

### Device Discovery

The HyperStudy TTL device can be reliably identified by USB VID/PID:
- **Vendor ID (VID):** `0x239A` (9242 decimal)
- **Product ID (PID):** `0x80F1` (32497 decimal)

This allows the bridge to find the device automatically, even when macOS assigns different port numbers (e.g., `/dev/cu.usbmodem101` vs `/dev/cu.usbmodem2101`).

### Bridge Configuration

**Option 1: Auto-discovery (Recommended)**

Use the provided Python script to find the device:

```bash
python3 /path/to/hyperstudy-ttl/testing/find_ttl_port.py
```

This returns the current port path, which can be used by the bridge.

**Option 2: Manual port identification**

   **macOS:**
   ```bash
   # Use cu.* ports for outgoing serial communication
   ls /dev/cu.usb*
   # Example: /dev/cu.usbmodem2101
   ```

   **Linux:**
   ```bash
   ls /dev/ttyACM*
   # Example: /dev/ttyACM0
   ```

   **Windows:**
   ```bash
   # Check Device Manager → Ports (COM & LPT)
   # Example: COM3
   ```

**Configure the bridge:**

In your `hyperstudy-bridge` application, configure the TTL device with either:
- Device discovery by VID/PID (preferred)
- The specific serial port path

**Test the bridge connection:**

The bridge should connect to the RP2040 and be able to send pulse commands.

### Communication Protocol

The firmware expects commands via USB serial (115200 baud):

**Command format:** `COMMAND\n` (newline-terminated, case-insensitive)

**Bridge-compatible responses:**
- Success: `OK:Message`
- Error: `ERROR:Message`

### HyperStudy TriggerComponent Integration

In your HyperStudy experiment configuration:

1. Configure a **TriggerComponent** with mode set to use the bridge
2. The TriggerComponent will communicate with `hyperstudy-bridge` via WebSocket (port 9000)
3. The bridge forwards the trigger to this RP2040 device via USB serial
4. The RP2040 sends the TTL pulse

**Latency:** Typical round-trip latency is <1ms for scientific timing accuracy.

## Part 4: Troubleshooting

### Device Not Detected

**Symptom:** Serial port doesn't appear

**Solutions:**
- Reconnect USB cable
- Try different USB port
- Check that Feather RP2040 is powered (LED should be on)
- On Linux: Check permissions (`sudo chmod 666 /dev/ttyACM0`)

### Bridge Can't Connect

**Symptom:** Bridge shows connection timeout

**Solutions:**
- Verify correct serial port in bridge configuration
- Close other applications using the serial port (Arduino IDE, serial monitors, etc.)
- Restart the bridge application
- Reflash the firmware

### No TTL Output

**Symptom:** Device responds to commands but no output on BNC

**Solutions:**
- Verify optocoupler wiring (see OPTOCOUPLER_WIRING.md)
- Test with multimeter: Pin 5 should go HIGH (3.3V) during pulse
- Check isolated power supply (5V on HCPL Pin 8)
- Verify 330Ω resistor is in place
- Check BNC cable connection

### High Latency (>1ms)

**Symptom:** Bridge reports latency warnings

**Solutions:**
- Close other USB devices and applications
- Use USB 2.0 port (sometimes more stable than USB 3.0)
- Check for USB hub issues (connect directly to computer)
- Verify 115200 baud rate is configured correctly

### Commands Not Recognized

**Symptom:** Device responds with `ERROR:Unknown command`

**Solutions:**
- Verify newline-terminated commands (`PULSE\n`)
- Check for extra whitespace or special characters
- Confirm firmware version supports the command (`VERSION`)
- Reflash firmware if responses are garbled

## Part 5: Testing Scripts

Python scripts are provided in `/testing` for device validation:

```bash
# Detect RP2040 on serial ports
python testing/detect_device.py

# Send test pulse and measure latency
python testing/test_pulse.py

# Validate bridge connection
python testing/validate_bridge.py
```

## Advanced Configuration

### Changing Pulse Duration

Pulse duration can be configured at runtime without reflashing:

**Via serial command (temporary, until reboot):**
```
SETDURATION 20
```

**Via inline parameter (per-pulse):**
```
PULSE 20
```

**Via hyperstudy-bridge:** Configure `pulse_duration_ms` in the TTL device settings. The bridge sends the duration with each PULSE command.

**Permanently (in firmware):** Edit `firmware/src/main.cpp`:
```cpp
#define DEFAULT_PULSE_DURATION_MS 10  // Change default duration in milliseconds
```
Then rebuild and upload: `cd firmware && pio run --target upload`

### Using Alternative Firmware

See `/examples` directory for Arduino IDE and CircuitPython implementations.

**Note:** Alternative firmwares may not be fully compatible with hyperstudy-bridge response parsing.

## Support

For issues specific to:
- **This firmware:** Open issue in this repository
- **Bridge integration:** See hyperstudy-bridge documentation
- **HyperStudy experiments:** See HyperStudy documentation
