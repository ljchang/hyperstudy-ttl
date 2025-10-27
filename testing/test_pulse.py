#!/usr/bin/env python3
"""
RP2040 TTL Pulse Latency Testing Script

Tests the RP2040 TTL device by sending multiple PULSE commands
and measuring latency statistics.
"""

import serial
import time
import sys
import argparse
import statistics


def measure_pulse_latency(port, num_pulses=10, interval=0.1):
    """
    Send multiple PULSE commands and measure latency.

    Args:
        port (str): Serial port name
        num_pulses (int): Number of pulses to send
        interval (float): Time between pulses in seconds

    Returns:
        list: List of latency measurements in milliseconds
    """
    latencies = []

    try:
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(0.5)  # Allow connection to stabilize

        print(f"Sending {num_pulses} pulses with {interval}s interval...")
        print("-" * 60)

        for i in range(num_pulses):
            # Clear buffers
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # Measure round-trip time
            start_time = time.time()
            ser.write(b"PULSE\n")

            # Wait for response
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            elapsed_ms = (time.time() - start_time) * 1000

            if response == "OK:Pulse sent":
                latencies.append(elapsed_ms)
                print(f"Pulse {i+1:2d}/{num_pulses}: {elapsed_ms:6.2f} ms ✓")
            else:
                print(f"Pulse {i+1:2d}/{num_pulses}: ERROR - Response: {response}")

            # Wait before next pulse
            if i < num_pulses - 1:
                time.sleep(interval)

        ser.close()

    except serial.SerialException as e:
        print(f"\nSerial connection error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nTest error: {e}")
        sys.exit(1)

    return latencies


def print_statistics(latencies):
    """
    Print latency statistics.

    Args:
        latencies (list): List of latency measurements in milliseconds
    """
    if not latencies:
        print("\nNo successful measurements!")
        return

    print("\n" + "=" * 60)
    print("LATENCY STATISTICS")
    print("=" * 60)
    print(f"Total pulses: {len(latencies)}")
    print(f"Mean latency: {statistics.mean(latencies):.2f} ms")
    print(f"Median latency: {statistics.median(latencies):.2f} ms")
    print(f"Min latency: {min(latencies):.2f} ms")
    print(f"Max latency: {max(latencies):.2f} ms")

    if len(latencies) > 1:
        print(f"Std deviation: {statistics.stdev(latencies):.2f} ms")

    # Check if latency meets requirements
    print("\n" + "-" * 60)
    print("PERFORMANCE ASSESSMENT")
    print("-" * 60)

    max_latency = max(latencies)
    mean_latency = statistics.mean(latencies)

    if max_latency < 1.0:
        print(f"✓ EXCELLENT - Max latency {max_latency:.2f} ms < 1 ms")
    elif max_latency < 5.0:
        print(f"✓ GOOD - Max latency {max_latency:.2f} ms < 5 ms")
    elif max_latency < 10.0:
        print(f"⚠ ACCEPTABLE - Max latency {max_latency:.2f} ms < 10 ms")
    else:
        print(f"✗ POOR - Max latency {max_latency:.2f} ms > 10 ms")
        print("  Consider:")
        print("  - Using a USB 2.0 port instead of USB 3.0")
        print("  - Connecting directly to computer (not via hub)")
        print("  - Closing other applications using USB")

    if mean_latency < 1.0:
        print(f"✓ Mean latency {mean_latency:.2f} ms is excellent")
    elif mean_latency < 2.0:
        print(f"✓ Mean latency {mean_latency:.2f} ms is good")
    else:
        print(f"⚠ Mean latency {mean_latency:.2f} ms may affect timing precision")


def main():
    parser = argparse.ArgumentParser(
        description='Test RP2040 TTL device pulse latency'
    )
    parser.add_argument(
        '--port',
        type=str,
        help='Serial port (e.g., /dev/ttyACM0 or COM3). If not specified, will auto-detect.'
    )
    parser.add_argument(
        '--num-pulses',
        type=int,
        default=10,
        help='Number of pulses to send (default: 10)'
    )
    parser.add_argument(
        '--interval',
        type=float,
        default=0.1,
        help='Interval between pulses in seconds (default: 0.1)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("HyperStudy TTL Pulse Latency Test")
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
            print("  python test_pulse.py --port /dev/ttyACM0")
            sys.exit(1)

        args.port = rp2040_port

    print(f"\nTesting device on port: {args.port}")
    print(f"Number of pulses: {args.num_pulses}")
    print(f"Interval: {args.interval}s")
    print()

    print("WARNING: This will trigger actual TTL pulses!")
    print("Make sure no sensitive equipment is connected unless you intend to trigger it.")
    print()

    try:
        response = input("Continue? (y/n): ").strip().lower()
        if response != 'y':
            print("Aborted.")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)

    print()

    # Run the test
    latencies = measure_pulse_latency(args.port, args.num_pulses, args.interval)

    # Print statistics
    print_statistics(latencies)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
