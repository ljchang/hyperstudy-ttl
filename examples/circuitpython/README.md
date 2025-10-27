# CircuitPython Example

This is an alternative firmware implementation using CircuitPython.

**Note:** This is provided as an example only. The **recommended** firmware is in `/firmware` (PlatformIO).

## Compatibility Notes

- Python-based, no compilation needed
- Slower response time than C++ implementations
- Easier to debug and modify on-device
- Response format has extra space: `"OK: Pulse Triggered!\n"` (may not parse correctly in bridge)

## Usage

1. Install CircuitPython on your Feather RP2040
2. Copy `code.py` to the CIRCUITPY drive
3. Device will auto-restart with new code

## Configuration

You may need to create `settings.toml` on CIRCUITPY for WebUSB origin configuration:

```toml
CIRCUITPY_USB_VENDOR = 0x239A
CIRCUITPY_USB_PRODUCT = 0x80F1
```

## Limitations

- Response format not fully compatible with hyperstudy-bridge parsing
- Slightly higher latency than compiled C++ firmware
- Requires CircuitPython 9+ for WebUSB support
