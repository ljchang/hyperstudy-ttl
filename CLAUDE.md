# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HyperStudy TTL is RP2040 firmware that receives trigger commands from hyperstudy-bridge and generates electrically-isolated TTL pulses for laboratory equipment. This is part of the HyperStudy experiment platform.

## Architecture

### Communication Flow
```
HyperStudy TriggerComponent → hyperstudy-bridge → RP2040 (this firmware) → TTL Output
```

1. **TriggerComponent** (Svelte component in HyperStudy frontend) sends trigger request
2. **hyperstudy-bridge** (Tauri app) receives WebSocket message on port 9000
3. **Bridge TtlDevice** sends `b"PULSE\n"` via USB serial (115200 baud)
4. **RP2040 firmware** (this repo) sets GPIO Pin 5 HIGH for 10ms
5. **HCPL-2211 optocoupler** provides electrical isolation to external equipment

### Primary Firmware (firmware/src/main.cpp)

**PlatformIO-based C++ implementation** - This is the recommended production firmware.

**Key specifications:**
- GPIO Pin 5 for TTL output
- Signal logic: LOW = off, HIGH = pulse active (10ms)
- USB serial: 115200 baud, newline-terminated commands
- Response format: `OK:Message` (success) or `ERROR:Message` (failure)
- USB identification: VID `0x239A`, PID `0x80F1` (for device discovery)

**Supported commands:**
- `PULSE` (case-insensitive) → Triggers pulse, responds `OK:Pulse sent`
- `TEST` → Connection test, responds `OK:Test successful`
- `VERSION` → Returns firmware version, responds `OK:Version 1.0.0`

**Bridge compatibility requirements:**
- Response format MUST match `OK:` prefix (bridge parses this)
- Command acceptance MUST include "PULSE" (what bridge sends)
- Latency MUST be <1ms for scientific timing accuracy

## Build Commands

### Primary Build (PlatformIO)
```bash
cd firmware
pio run --target upload
```

### Test Firmware
```bash
cd firmware
pio device monitor
# Type: PULSE
# Expected: OK:Pulse sent
```

### Alternative Implementations
Located in `/examples` for reference only (NOT for production use):
- **Arduino IDE**: `examples/arduino/arduino_sketch_hyperstudyttl.ino`
- **CircuitPython**: `examples/circuitpython/code.py`

These alternatives have different response formats and may not be fully compatible with hyperstudy-bridge.

## Repository Structure

```
/firmware              # Primary PlatformIO firmware (PRODUCTION)
/examples              # Alternative implementations (REFERENCE ONLY)
  /arduino             # Arduino IDE version
  /circuitpython       # CircuitPython version
/testing               # Python scripts for device validation
INSTALLATION.md        # Complete setup guide
OPTOCOUPLER_WIRING.md  # Hardware wiring instructions
README.md              # Project overview
```

## Important Notes

### When Modifying Firmware
- **Maintain bridge compatibility**: Response format `OK:` prefix is critical
- **Preserve timing**: 10ms pulse duration is standard for lab equipment
- **Keep latency low**: <1ms round-trip for scientific accuracy
- **Test with bridge**: Don't just test serial commands, verify bridge integration

### Signal Logic
- **LOW (0V)** = Signal OFF (idle state)
- **HIGH (3.3V)** = Signal ON (pulse active)
- Optocoupler inverts this to 5V TTL output

### Electrical Isolation
The HCPL-2211 optocoupler provides galvanic isolation between the RP2040 and external equipment. **Input and output grounds MUST be separate** for proper isolation.

### No WebUSB Direct Connection
This firmware is designed for **bridge-based communication only**. Previous WebUSB direct browser integration has been removed in favor of the more reliable bridge architecture.

### Testing
Use provided Python scripts in `/testing` directory for:
- Device detection and enumeration (`detect_device.py`)
- Latency measurement (`test_pulse.py`)
- Bridge connection validation (`validate_bridge.py`)
- Port discovery by VID/PID (`find_ttl_port.py`)

### Device Discovery
The device can be reliably found by USB VID/PID (VID: `0x239A`, PID: `0x80F1`) regardless of which port number the OS assigns. Use `testing/find_ttl_port.py` to get the current port path.
