# HyperStudy TTL

A project to trigger a TTL pulse on a Feather RP2040 over WebUSB using a browser.

## Features

- WebUSB interface for in-browser triggering
- Optocoupler-isolated TTL pulse
- Custom landing page on GitHub Pages

## Setup

### Flash the Firmware

1. Install [PlatformIO](https://platformio.org/)
2. Connect the Feather RP2040
3. Run:

```bash
cd firmware
pio run --target upload
```

### Serve the Landing Page

This repo is configured to work with GitHub Pages.

- URL: https://cosanlab.github.io/hyperstudy-ttl/web

### Use It

1. Visit the landing page
2. Click “Connect”
3. Click “Send TTL Pulse”

## Wiring Guide

🔌 Step-by-Step Wiring Guide

🟦 1. Power Rails
• Red Breadboard Rail (3.3V) ← Connect from Feather 3.3V pin
• Blue Breadboard Rail (GND) ← Connect from Feather GND pin
• Create a second isolated power rail for the HCPL output side:
• Use Feather’s USB pin (5V) to power the output Vcc
• Use a second GND rail for the isolated side

🧠 The input and output grounds must be separate to maintain isolation!

⸻

🔶 2. Input Side (Feather → HCPL-2211)
• GPIO pin (e.g. D4) → One leg of 330Ω resistor
• Other leg of resistor → HCPL-2211 Pin 2 (Anode)
• HCPL-2211 Pin 3 (Cathode) → Feather GND

✅ This drives the optocoupler’s internal LED when D5 is HIGH.

⸻

🔷 3. Output Side (HCPL-2211 → BNC Trigger)
• HCPL-2211 Pin 8 → 5V rail (from Feather’s USB pin or other 5V source)
• HCPL-2211 Pin 5 → GND (isolated side) (do NOT connect to Feather GND!)
• HCPL-2211 Pin 6 (Output) → BNC center pin
• BNC shield (outer) → Isolated GND rail

⚡ Now, when the Feather sends a signal, the HCPL output drives a 5V TTL pulse to the BNC — fully isolated!

⸻

✅ Final Notes
• Add a 0.1 µF capacitor between HCPL pins 8 and 5 (Vcc/GND) near the chip.
• Keep the signal wires short and clean.
• Check the BNC pinout — center is signal, outer is ground.

## Circuit Python

https://circuitpython.org/board/adafruit_feather_rp2040/
