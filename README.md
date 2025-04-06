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

Enjoy!
