#!/usr/bin/env python3
"""
RP2040 TTL Device Detection Script

Scans serial ports to find the HyperStudy TTL device.
Identifies the device by sending a VERSION command and checking the response.
"""

import serial
import serial.tools.list_ports
import time
import sys


def find_rp2040_device():
    """
    Scan all available serial ports to find the RP2040 TTL device.

    Returns:
        tuple: (port_name, device_info) if found, (None, None) otherwise
    """
    print("Scanning for RP2040 TTL device...")
    print("-" * 60)

    ports = serial.tools.list_ports.comports()

    if not ports:
        print("No serial ports found!")
        return None, None

    print(f"Found {len(ports)} serial port(s):\n")

    for port in ports:
        print(f"Port: {port.device}")
        print(f"  Description: {port.description}")
        print(f"  Manufacturer: {port.manufacturer}")
        print(f"  VID:PID: {port.vid:04X}:{port.pid:04X}" if port.vid else "  VID:PID: N/A")

        # Check if it's a Feather RP2040 (Adafruit vendor ID)
        if port.vid == 0x239A:
            print("  → Potential Feather RP2040 detected!")

            # Try to connect and verify
            try:
                print("  → Attempting to connect...")
                ser = serial.Serial(port.device, 115200, timeout=2)
                time.sleep(0.5)  # Wait for connection to stabilize

                # Clear any existing data
                ser.reset_input_buffer()
                ser.reset_output_buffer()

                # Send VERSION command
                ser.write(b"VERSION\n")
                time.sleep(0.1)

                # Read response
                response = ser.readline().decode('utf-8', errors='ignore').strip()

                if response.startswith("OK:Version"):
                    version = response.replace("OK:Version ", "")
                    print(f"  → ✓ HyperStudy TTL Device Found!")
                    print(f"  → Firmware Version: {version}")
                    ser.close()
                    return port.device, {
                        'port': port.device,
                        'version': version,
                        'description': port.description,
                        'manufacturer': port.manufacturer
                    }
                else:
                    print(f"  → Device responded but not recognized: {response}")
                    ser.close()

            except serial.SerialException as e:
                print(f"  → Connection failed: {e}")
            except Exception as e:
                print(f"  → Error: {e}")

        print()

    return None, None


def test_device_connection(port):
    """
    Test the device connection by sending TEST and PULSE commands.

    Args:
        port (str): Serial port name
    """
    print(f"\nTesting device on {port}...")
    print("-" * 60)

    try:
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(0.5)

        # Test 1: TEST command
        print("Test 1: Sending TEST command...")
        ser.reset_input_buffer()
        ser.write(b"TEST\n")
        time.sleep(0.1)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  Response: {response}")

        if response == "OK:Test successful":
            print("  ✓ PASS")
        else:
            print("  ✗ FAIL - Unexpected response")

        # Test 2: VERSION command
        print("\nTest 2: Sending VERSION command...")
        ser.reset_input_buffer()
        ser.write(b"VERSION\n")
        time.sleep(0.1)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"  Response: {response}")

        if response.startswith("OK:Version"):
            print("  ✓ PASS")
        else:
            print("  ✗ FAIL - Unexpected response")

        # Test 3: PULSE command (warning - this will trigger TTL output!)
        print("\nTest 3: Sending PULSE command...")
        print("  WARNING: This will trigger a 10ms TTL pulse!")
        ser.reset_input_buffer()

        start_time = time.time()
        ser.write(b"PULSE\n")
        time.sleep(0.1)
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        elapsed_ms = (time.time() - start_time) * 1000

        print(f"  Response: {response}")
        print(f"  Round-trip time: {elapsed_ms:.2f} ms")

        if response == "OK:Pulse sent":
            print("  ✓ PASS")
            if elapsed_ms < 50:
                print(f"  ✓ Latency acceptable ({elapsed_ms:.2f} ms)")
            else:
                print(f"  ⚠ Latency high ({elapsed_ms:.2f} ms)")
        else:
            print("  ✗ FAIL - Unexpected response")

        ser.close()
        print("\n" + "=" * 60)
        print("All tests completed!")

    except serial.SerialException as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test error: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("HyperStudy TTL Device Detection & Testing")
    print("=" * 60)
    print()

    port, info = find_rp2040_device()

    if port:
        print("\n" + "=" * 60)
        print("DEVICE FOUND")
        print("=" * 60)
        print(f"Port: {port}")
        print(f"Version: {info['version']}")
        print()

        # Ask user if they want to run tests
        try:
            response = input("Run connection tests? (y/n): ").strip().lower()
            if response == 'y':
                test_device_connection(port)
        except KeyboardInterrupt:
            print("\n\nAborted by user.")
            sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("NO HYPERSTUDY TTL DEVICE FOUND")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Check that the RP2040 is connected via USB")
        print("2. Verify the firmware is flashed (see INSTALLATION.md)")
        print("3. Try a different USB cable or port")
        print("4. On Linux, check permissions: sudo chmod 666 /dev/ttyACM0")
        sys.exit(1)


if __name__ == "__main__":
    main()
