#!/usr/bin/env python3
"""
Find HyperStudy TTL Device Port

Finds the serial port for the HyperStudy TTL device by USB VID/PID,
regardless of which /dev/cu.usbmodemXXXX number macOS assigns.

Device identification:
- VID: 0x239A (Adafruit)
- PID: 0x80F1 (HyperStudy TTL custom product ID)

Usage:
    python3 find_ttl_port.py

Returns:
    Port path (e.g., /dev/cu.usbmodem2101) on stdout if found
    Exit code 0 on success, 1 on failure
"""

import serial.tools.list_ports
import sys


def find_hyperstudy_ttl_port():
    """
    Find the HyperStudy TTL device by USB VID:PID (239A:80F1).

    Returns:
        str: Port path (e.g., /dev/cu.usbmodem2101) or None if not found
    """
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Check for Adafruit VID (0x239A) and our custom PID (0x80F1)
        if port.vid == 0x239A and port.pid == 0x80F1:
            return port.device

    return None


if __name__ == "__main__":
    port = find_hyperstudy_ttl_port()

    if port:
        print(port)
        sys.exit(0)
    else:
        print("ERROR: HyperStudy TTL device not found", file=sys.stderr)
        print("Make sure the device is connected via USB", file=sys.stderr)
        sys.exit(1)
