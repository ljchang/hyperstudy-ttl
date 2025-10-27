# Arduino IDE Example

This is an alternative firmware implementation using the Arduino IDE.

**Note:** This is provided as an example only. The **recommended** firmware is in `/firmware` (PlatformIO).

## Compatibility Notes

- Uses emoji in responses (not parsed by hyperstudy-bridge)
- Different pin logic than primary firmware
- Easier for beginners to modify without PlatformIO

## Usage

1. Open `arduino_sketch_hyperstudyttl.ino` in Arduino IDE
2. Install Adafruit TinyUSB library
3. Select "Adafruit Feather RP2040" board
4. Upload to device

## Limitations

- Response format not fully compatible with hyperstudy-bridge parsing
- May require bridge code modifications to work correctly
