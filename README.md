# HyperStudy TTL

RP2040-based TTL pulse generator for HyperStudy experiments with electrical isolation via optocoupler.

## Architecture

```
HyperStudy TriggerComponent → hyperstudy-bridge → RP2040 (this firmware) → TTL Output
```

This repository contains the **RP2040 firmware** that receives trigger commands from [hyperstudy-bridge](https://github.com/cosanlab/hyperstudy-bridge) and generates electrically-isolated 10ms TTL pulses for external equipment.

## Features

- **Fast & Reliable:** <1ms latency via USB serial communication
- **Electrical Isolation:** HCPL-2211 optocoupler protects both devices
- **Bridge Compatible:** Response format matches hyperstudy-bridge parser expectations
- **Easy Setup:** PlatformIO-based firmware with comprehensive installation docs

## Quick Start

### 1. Install Firmware

```bash
cd firmware
pio run --target upload
```

### 2. Test Connection

```bash
pio device monitor
```

Type `PULSE` and press Enter. The device should respond with `OK:Pulse sent`.

### 3. Full Setup

See **[INSTALLATION.md](./INSTALLATION.md)** for complete instructions including:
- Hardware assembly and optocoupler wiring
- Bridge integration and configuration
- TriggerComponent setup in HyperStudy
- Troubleshooting guide

## Hardware

- **Microcontroller:** Adafruit Feather RP2040
- **Optocoupler:** HCPL-2211 (for isolation)
- **Pulse Output:** GPIO Pin 5 (10ms HIGH pulse)
- **Communication:** USB serial, 115200 baud
- **USB Identification:** VID: `0x239A`, PID: `0x80F1`

See [OPTOCOUPLER_WIRING.md](./OPTOCOUPLER_WIRING.md) for detailed wiring instructions.

## Commands

The firmware accepts case-insensitive serial commands:

| Command | Response | Description |
|---------|----------|-------------|
| `PULSE` | `OK:Pulse sent` | Triggers 10ms TTL pulse |
| `TEST` | `OK:Test successful` | Connection validation |
| `VERSION` | `OK:Version 1.0.2` | Firmware version query |

## Device Discovery

The device can be reliably found by USB VID/PID, regardless of which port macOS assigns:

```python
# Find device by VID/PID (works with any HyperStudy TTL device)
python3 testing/find_ttl_port.py
```

This returns the current port path (e.g., `/dev/cu.usbmodem2101`).

## Alternative Implementations

Alternative firmwares (Arduino IDE, CircuitPython) are provided in `/examples` for reference but are **not recommended** for production use as they may not be fully compatible with hyperstudy-bridge.

## Documentation

- **[INSTALLATION.md](./INSTALLATION.md)** - Complete setup guide with bridge integration
- **[OPTOCOUPLER_WIRING.md](./OPTOCOUPLER_WIRING.md)** - Detailed optocoupler wiring instructions
- **[CLAUDE.md](./CLAUDE.md)** - Developer notes and architecture details

## Support

For detailed user documentation on using TTL triggers in HyperStudy experiments, see the [HyperStudy documentation](https://github.com/cosanlab/hyperstudy).
