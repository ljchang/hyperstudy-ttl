#!/usr/bin/env python3
"""
HyperStudy Bridge Connection Validator

Validates that the RP2040 TTL device is compatible with hyperstudy-bridge
by testing the exact command format and response parsing that the bridge uses.
"""

import serial
import time
import sys
import argparse


def validate_bridge_protocol(port):
    """
    Test the exact protocol used by hyperstudy-bridge.

    The bridge sends: b"PULSE\n"
    The bridge expects: "OK:Pulse sent"

    Args:
        port (str): Serial port name

    Returns:
        bool: True if validation passes, False otherwise
    """
    print("Validating bridge protocol compatibility...")
    print("-" * 60)

    try:
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(0.5)

        all_passed = True

        # Test 1: Exact bridge command format
        print("\nTest 1: Bridge PULSE command format")
        print("  Command: b'PULSE\\n'")
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        start_time = time.time()
        ser.write(b"PULSE\n")  # Exact format bridge uses
        time.sleep(0.02)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        elapsed_ms = (time.time() - start_time) * 1000

        print(f"  Response: '{response}'")
        print(f"  Latency: {elapsed_ms:.2f} ms")

        if response == "OK:Pulse sent":
            print("  ✓ PASS - Response format matches bridge expectations")
        else:
            print("  ✗ FAIL - Response does not match expected 'OK:Pulse sent'")
            all_passed = False

        if elapsed_ms > 1.0:
            print(f"  ⚠ WARNING - Latency {elapsed_ms:.2f} ms exceeds 1ms target")

        # Test 2: Response parsing (check for exact format)
        print("\nTest 2: Response format validation")
        if response.startswith("OK:"):
            print("  ✓ PASS - Response has 'OK:' prefix")
        else:
            print("  ✗ FAIL - Response missing 'OK:' prefix")
            all_passed = False

        if ":" in response:
            parts = response.split(":", 1)
            if len(parts) == 2:
                status, message = parts
                print(f"  Status: '{status}'")
                print(f"  Message: '{message}'")
                print("  ✓ PASS - Response is parseable")
            else:
                print("  ✗ FAIL - Response format incorrect")
                all_passed = False
        else:
            print("  ✗ FAIL - Response missing ':' separator")
            all_passed = False

        # Test 3: Case insensitivity (bridge might send lowercase)
        print("\nTest 3: Case insensitivity check")
        print("  Command: b'pulse\\n' (lowercase)")
        ser.reset_input_buffer()
        ser.write(b"pulse\n")
        time.sleep(0.02)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  Response: '{response}'")

        if response == "OK:Pulse sent":
            print("  ✓ PASS - Accepts lowercase commands")
        else:
            print("  ✗ FAIL - Does not accept lowercase")
            all_passed = False

        # Test 4: Connection test command
        print("\nTest 4: TEST command (for connection validation)")
        print("  Command: b'TEST\\n'")
        ser.reset_input_buffer()
        ser.write(b"TEST\n")
        time.sleep(0.02)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  Response: '{response}'")

        if response == "OK:Test successful":
            print("  ✓ PASS - TEST command supported")
        else:
            print("  ⚠ WARNING - TEST command not supported or wrong format")

        # Test 5: Invalid command handling
        print("\nTest 5: Error handling")
        print("  Command: b'INVALID\\n'")
        ser.reset_input_buffer()
        ser.write(b"INVALID\n")
        time.sleep(0.02)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  Response: '{response}'")

        if response.startswith("ERROR:"):
            print("  ✓ PASS - Errors use 'ERROR:' prefix")
        else:
            print("  ⚠ WARNING - Error format may not be parseable by bridge")

        ser.close()

        return all_passed

    except serial.SerialException as e:
        print(f"\nSerial connection error: {e}")
        return False
    except Exception as e:
        print(f"\nValidation error: {e}")
        return False


def check_firmware_version(port):
    """
    Check firmware version to ensure it's compatible.

    Args:
        port (str): Serial port name

    Returns:
        str: Firmware version or None
    """
    try:
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(0.5)

        ser.reset_input_buffer()
        ser.write(b"VERSION\n")
        time.sleep(0.1)
        response = ser.readline().decode('utf-8', errors='ignore').strip()

        ser.close()

        if response.startswith("OK:Version"):
            version = response.replace("OK:Version ", "").strip()
            return version
        return None

    except:
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Validate RP2040 TTL device compatibility with hyperstudy-bridge'
    )
    parser.add_argument(
        '--port',
        type=str,
        help='Serial port (e.g., /dev/ttyACM0 or COM3). If not specified, will auto-detect.'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("HyperStudy Bridge Compatibility Validator")
    print("=" * 60)
    print()

    # Auto-detect if port not specified
    if not args.port:
        print("No port specified. Auto-detecting device...")
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()
        rp2040_port = None

        for port in ports:
            if port.vid == 0x239A:  # Adafruit vendor ID
                try:
                    ser = serial.Serial(port.device, 115200, timeout=1)
                    time.sleep(0.3)
                    ser.write(b"VERSION\n")
                    time.sleep(0.1)
                    response = ser.readline().decode('utf-8', errors='ignore').strip()
                    ser.close()

                    if response.startswith("OK:Version"):
                        rp2040_port = port.device
                        print(f"Found device on {port.device}")
                        break
                except:
                    continue

        if not rp2040_port:
            print("ERROR: Could not auto-detect device.")
            print("Please specify port with --port option.")
            print("\nExample:")
            print("  python validate_bridge.py --port /dev/ttyACM0")
            sys.exit(1)

        args.port = rp2040_port

    print(f"\nDevice port: {args.port}")

    # Check firmware version
    version = check_firmware_version(args.port)
    if version:
        print(f"Firmware version: {version}")
    else:
        print("WARNING: Could not determine firmware version")

    print()

    # Run validation
    passed = validate_bridge_protocol(args.port)

    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)

    if passed:
        print("✓ ALL TESTS PASSED")
        print("\nThis device is compatible with hyperstudy-bridge.")
        print("\nNext steps:")
        print("1. Configure the bridge with this serial port:")
        print(f"   Port: {args.port}")
        print("2. Restart hyperstudy-bridge if it's already running")
        print("3. Test trigger from HyperStudy TriggerComponent")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("\nThis device may not work correctly with hyperstudy-bridge.")
        print("\nTroubleshooting:")
        print("1. Reflash the firmware (see INSTALLATION.md)")
        print("2. Verify you're using the primary PlatformIO firmware")
        print("3. Check that firmware version is 1.0.0 or later")
        sys.exit(1)


if __name__ == "__main__":
    main()
