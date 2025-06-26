# code.py for Adafruit RP2040 - WebUSB TTL Pulse Trigger
# Using built-in WebUSB support in CircuitPython 9+ (via TinyUSB)

import board
import digitalio
import time
import usb_cdc  # Using only the built-in USB CDC module

print("Imports complete. Starting setup...")
print(
    f"Running CircuitPython {usb_cdc.CIRCUITPYTHON_VERSION}"
)  # Good practice to log version

# --- Configuration ---
TTL_PIN = board.D5
PULSE_DURATION_MS = 10
TRIGGER_COMMAND = "PULSE"

# --- WebUSB Configuration Note ---
# With built-in WebUSB, allowed origins might be set in your
# CIRCUITPY/settings.toml file, not in this code.
# Check CircuitPython 9+ documentation for configuring USB descriptors
# and WebUSB settings if you need to restrict origins.
print("NOTE: WebUSB Allowed Origins might need configuration in settings.toml")

# --- Setup Pin ---
ttl_pin = digitalio.DigitalInOut(TTL_PIN)
ttl_pin.direction = digitalio.Direction.OUTPUT
ttl_pin.value = False
print(f"TTL Output Pin: {TTL_PIN} configured.")
print(f"Pulse Duration: {PULSE_DURATION_MS} ms")

# --- Setup & Check USB CDC Serial ---
# CircuitPython typically enables usb_cdc automatically.
# We prefer using 'usb_cdc.data' if the board provides a separate data channel.
serial_port = None
if usb_cdc.data:
    serial_port = usb_cdc.data
    print("Communication configured to use: usb_cdc.data")
else:
    # If no separate usb_cdc.data, communication might mix with the REPL
    # on usb_cdc.console. This can be tricky.
    # Let's print a warning and proceed assuming console might work, or user
    # needs a board with a dedicated data port for robust communication.
    print("WARNING: No separate usb_cdc.data found.")
    print("Communication might use usb_cdc.console (REPL).")
    print("Input/output might be interleaved with REPL messages.")
    serial_port = usb_cdc.console  # Fallback to console - use with caution

print(f"Waiting for connection and '{TRIGGER_COMMAND}' command via USB CDC...")


# --- Pulse Function ---
def trigger_ttl_pulse():
    print("--> Triggering Pulse!")
    try:
        ttl_pin.value = True
        time.sleep(PULSE_DURATION_MS / 1000.0)
        ttl_pin.value = False
        print("<-- Pulse Complete.")
    except Exception as e:
        print(f"Error during pulse: {e}")
        ttl_pin.value = False  # Ensure pin is low


# --- Main Loop ---
input_buffer = ""

while True:
    # Use the determined serial port object
    if serial_port and serial_port.connected:
        bytes_available = serial_port.in_waiting
        if bytes_available > 0:
            try:
                data_bytes = serial_port.read(bytes_available)
                # Append received bytes, decoded, to buffer
                input_buffer += data_bytes.decode("utf-8")

                # Check if a newline indicates end of command (process line by line)
                if "\n" in input_buffer:
                    # Split buffer, process first command, keep remainder
                    command_string, input_buffer = input_buffer.split("\n", 1)
                    command_string = command_string.strip()  # Clean command

                    if command_string:  # Ignore empty lines
                        print(f"Received command: '{command_string}'")

                        if command_string == TRIGGER_COMMAND:
                            trigger_ttl_pulse()
                            serial_port.write(b"OK: Pulse Triggered!\n")
                        else:
                            print("Unknown command received.")
                            response = f"ERR: Unknown command '{command_string}'. Send '{TRIGGER_COMMAND}'.\n"
                            serial_port.write(response.encode("utf-8"))

            except UnicodeDecodeError:
                print("Received invalid (non-UTF-8) data.")
                try:
                    # Try sending error back even if buffer is corrupt
                    serial_port.write(b"ERR: Invalid data encoding.\n")
                except Exception:
                    pass  # Ignore write error
                input_buffer = ""  # Reset buffer on decode error
            except Exception as e:
                print(f"Error processing command: {e}")
                try:
                    serial_port.write(
                        b"ERR: Internal device error during processing.\n"
                    )
                except Exception:
                    pass  # Ignore write error
                input_buffer = ""  # Reset buffer on other errors too

    # Brief pause for background tasks
    time.sleep(0.01)
