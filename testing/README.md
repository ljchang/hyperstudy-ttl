# Testing Scripts

Python scripts for validating RP2040 TTL device functionality and bridge compatibility.

## Requirements

```bash
pip install pyserial
```

## Scripts

### 1. detect_device.py

Automatically scans serial ports to find the RP2040 TTL device.

**Usage:**
```bash
python detect_device.py
```

**Features:**
- Auto-detects Feather RP2040 devices
- Verifies firmware version
- Runs basic connection tests
- Reports device information

### 2. test_pulse.py

Measures TTL pulse latency by sending multiple PULSE commands and collecting statistics.

**Usage:**
```bash
# Auto-detect device
python test_pulse.py

# Specify port manually
python test_pulse.py --port /dev/ttyACM0

# Custom number of pulses
python test_pulse.py --num-pulses 100

# Custom interval between pulses
python test_pulse.py --interval 0.5
```

**Output:**
- Individual pulse latencies
- Statistical summary (mean, median, min, max, std dev)
- Performance assessment

**Warning:** This script triggers actual TTL pulses. Ensure no sensitive equipment is connected unless you intend to trigger it.

### 3. validate_bridge.py

Validates that the device is compatible with hyperstudy-bridge by testing the exact protocol the bridge uses.

**Usage:**
```bash
# Auto-detect device
python validate_bridge.py

# Specify port manually
python validate_bridge.py --port /dev/ttyACM0
```

**Tests:**
- Exact command format bridge uses (`b"PULSE\n"`)
- Response format parsing (`"OK:Pulse sent"`)
- Case insensitivity (accepts both "PULSE" and "pulse")
- TEST command support
- Error handling

## Typical Workflow

1. **First time setup:**
   ```bash
   python detect_device.py
   ```
   This will find your device and verify the firmware is loaded.

2. **Test latency performance:**
   ```bash
   python test_pulse.py --num-pulses 20
   ```
   This ensures latency is acceptable (<1ms for scientific accuracy).

3. **Validate bridge compatibility:**
   ```bash
   python validate_bridge.py
   ```
   This confirms the device will work with hyperstudy-bridge.

## Troubleshooting

### Permission Denied (Linux)

```bash
sudo chmod 666 /dev/ttyACM0
```

Or add yourself to the `dialout` group:
```bash
sudo usermod -a -G dialout $USER
# Then log out and back in
```

### Device Not Found

1. Verify RP2040 is connected via USB
2. Check that firmware is flashed (see INSTALLATION.md)
3. Try a different USB cable or port
4. On Windows, check Device Manager for COM port

### High Latency

- Use USB 2.0 port instead of USB 3.0
- Connect directly to computer (not via hub)
- Close other USB-intensive applications
- Try a different USB cable

## Example Output

```
$ python validate_bridge.py

============================================================
HyperStudy Bridge Compatibility Validator
============================================================

Found device on /dev/ttyACM0
Device port: /dev/ttyACM0
Firmware version: 1.0.0

Validating bridge protocol compatibility...
------------------------------------------------------------

Test 1: Bridge PULSE command format
  Command: b'PULSE\n'
  Response: 'OK:Pulse sent'
  Latency: 0.87 ms
  ✓ PASS - Response format matches bridge expectations

...

============================================================
VALIDATION RESULTS
============================================================
✓ ALL TESTS PASSED

This device is compatible with hyperstudy-bridge.
```
