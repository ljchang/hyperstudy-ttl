# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HyperStudy TTL is a hardware interface that enables browser-based triggering of TTL pulses through a Feather RP2040 microcontroller using WebUSB. The project provides three firmware implementations (PlatformIO/C++, Arduino, CircuitPython) and a web interface for control.

## Build Commands

### Primary Build (PlatformIO)
```bash
cd firmware
pio run --target upload
```

### Alternative Methods
- **Arduino IDE**: Load `sketch/arduino_sketch_hyperstudyttl.ino` and upload
- **CircuitPython**: Copy `circuitpython/code.py` to CIRCUITPY drive

## Architecture

### Hardware Communication Pattern
All firmware implementations follow the same pattern:
1. Listen for "pulse" command via USB serial
2. Set GPIO Pin 5 HIGH for 10ms
3. Return confirmation message
4. The hardware uses HCPL-2211 optocoupler for electrical isolation

### WebUSB Configuration
- Vendor ID: 0x239A (Adafruit)
- Product ID: 0x80F1
- Build flags in `platformio.ini` disable CDC and enable WebUSB
- No WebUSB landing page is configured (commented out)

### Cross-Implementation Consistency
When modifying firmware, ensure all three implementations maintain:
- GPIO Pin 5 for TTL output
- 10ms pulse duration
- "pulse" command trigger
- Response format with emoji confirmation

## Important Notes

- The web interface is deployed via GitHub Pages at https://cosanlab.github.io/hyperstudy-ttl/web
- CircuitPython implementation may require `settings.toml` for WebUSB origin configuration
- The project prioritizes electrical isolation for safety in laboratory environments