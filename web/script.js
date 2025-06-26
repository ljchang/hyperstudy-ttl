// WebSerial API implementation for HyperStudy TTL Controller
let port;
let reader;
let writer;
let readableStreamClosed;
let writableStreamClosed;

// UI Elements
const connectBtn = document.getElementById('connectBtn');
const pulseBtn = document.getElementById('pulseBtn');
const disconnectBtn = document.getElementById('disconnectBtn');
const statusDiv = document.getElementById('status');
const logDiv = document.getElementById('log');
const browserWarning = document.getElementById('browserWarning');

// Check if browser supports Web Serial API
if (!('serial' in navigator)) {
    browserWarning.style.display = 'block';
    connectBtn.disabled = true;
    log('Error: Web Serial API not supported in this browser', 'error');
}

// Logging function
function log(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const entry = `[${timestamp}] ${message}`;
    
    // Add to log div with appropriate styling
    const span = document.createElement('span');
    span.textContent = entry + '\n';
    span.className = type;
    logDiv.appendChild(span);
    
    // Auto-scroll to bottom
    logDiv.scrollTop = logDiv.scrollHeight;
    
    // Also log to console
    console.log(entry);
}

// Update connection status
function updateStatus(connected) {
    if (connected) {
        statusDiv.textContent = 'Connected';
        statusDiv.className = 'connected';
        connectBtn.disabled = true;
        pulseBtn.disabled = false;
        disconnectBtn.disabled = false;
    } else {
        statusDiv.textContent = 'Disconnected';
        statusDiv.className = 'disconnected';
        connectBtn.disabled = false;
        pulseBtn.disabled = true;
        disconnectBtn.disabled = true;
    }
}

// Connect to serial device
async function connectSerial() {
    try {
        // Request a port and open a connection
        port = await navigator.serial.requestPort({
            filters: [
                { usbVendorId: 0x239A }, // Adafruit vendor ID
            ]
        });
        
        // Get port info
        const info = port.getInfo();
        log(`Selected port: VID=0x${info.usbVendorId.toString(16)}, PID=0x${info.usbProductId.toString(16)}`, 'info');
        
        // Open the serial port
        await port.open({ baudRate: 115200 });
        
        log('Port opened successfully', 'success');
        
        // Setup the reader and writer
        const textEncoder = new TextEncoderStream();
        writableStreamClosed = textEncoder.readable.pipeTo(port.writable);
        writer = textEncoder.writable.getWriter();
        
        const textDecoder = new TextDecoderStream();
        readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
        reader = textDecoder.readable.getReader();
        
        // Start reading from the serial port
        readLoop();
        
        updateStatus(true);
        log('Connected to Feather RP2040', 'success');
        
        // Send a test command
        await sendCommand('test');
        
    } catch (error) {
        log(`Connection failed: ${error.message}`, 'error');
        updateStatus(false);
    }
}

// Read data from serial port
async function readLoop() {
    try {
        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                reader.releaseLock();
                break;
            }
            if (value) {
                // Process received data
                const lines = value.trim().split('\n');
                for (const line of lines) {
                    if (line) {
                        log(`Device: ${line}`, line.includes('OK') ? 'success' : 'info');
                    }
                }
            }
        }
    } catch (error) {
        log(`Read error: ${error.message}`, 'error');
    }
}

// Send command to device
async function sendCommand(command) {
    if (!writer) {
        log('Not connected to device', 'error');
        return;
    }
    
    try {
        await writer.write(command + '\n');
        log(`Sent: ${command}`, 'info');
    } catch (error) {
        log(`Send error: ${error.message}`, 'error');
    }
}

// Send pulse command
async function sendPulse() {
    pulseBtn.disabled = true;
    await sendCommand('pulse');
    
    // Re-enable button after a short delay
    setTimeout(() => {
        pulseBtn.disabled = false;
    }, 500);
}

// Disconnect from serial device
async function disconnectSerial() {
    try {
        if (reader) {
            await reader.cancel();
            await readableStreamClosed.catch(() => {});
        }
        if (writer) {
            await writer.close();
            await writableStreamClosed;
        }
        if (port) {
            await port.close();
        }
        
        reader = null;
        writer = null;
        port = null;
        
        updateStatus(false);
        log('Disconnected from device', 'info');
        
    } catch (error) {
        log(`Disconnect error: ${error.message}`, 'error');
    }
}

// Event listeners
connectBtn.addEventListener('click', () => {
    document.getElementById('portInfo').style.display = 'block';
    connectSerial();
});
pulseBtn.addEventListener('click', sendPulse);
disconnectBtn.addEventListener('click', disconnectSerial);

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (port) {
        disconnectSerial();
    }
});

// Initialize
log('HyperStudy TTL Controller ready', 'info');
log('Click "Connect Device" to begin', 'info');