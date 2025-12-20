# HCPL-2211 Optocoupler Wiring Guide

## HCPL-2211 Pinout (from datasheet)

```
        ┌───∪───┐
NC ─────┤1     8├───── VCC (4.5-20V)
ANODE ──┤2     7├───── VO (Output)
CATHODE─┤3     6├───── NC
NC ─────┤4     5├───── GND
        └───────┘
```

**Key features:**
- Totem pole output (no pull-up resistor needed)
- Non-inverting: LED ON = Output HIGH, LED OFF = Output LOW
- Wide VCC range: 4.5V to 20V

## Circuit Diagram

```
Feather RP2040 Side                     Isolated Output Side

                    HCPL-2211                    DC Isolator
                   ┌─────────┐                  ┌─────────┐
        NC ────────┤1      8 ├──────────────────┤ +Out    │
                   │         │       │          │         │
GPIO 6 ──[220Ω]───┤2 (A)  7 ├──[47Ω]──► BNC+   │  5V     │
                   │         │                  │ Isolated│
Feather GND ──────┤3 (K)  6 ├── NC             │         │
                   │         │                  │         │
        NC ────────┤4      5 ├──────────────────┤ -Out    ├──► BNC-
                   └─────────┘       │          └─────────┘
                                     │               │
                              [0.1µF ceramic]   [0.1µF cer]
                              [10µF electro]    (on input)
                                     │               │
                                    GND            GND

Legend:
- A = Anode (LED +)
- K = Cathode (LED -)
- [220Ω] = Input current limiting resistor
- [47Ω] = Output series resistor (impedance matching)
- [0.1µF] = Ceramic bypass capacitor
- [10µF] = Electrolytic bulk capacitor
```

## Component Values

### Input Side

1. **R1 (LED Current Limiting): 220Ω**
   - Calculation: (3.3V - 1.5V) / 220Ω ≈ 8mA
   - Provides fast switching response
   - Within safe operating range for pulsed operation

### Output Side

2. **R2 (Series Output Resistor): 47Ω**
   - Impedance matching for BNC cable (50Ω nominal)
   - Optional but recommended for signal integrity

3. **C1 (Bypass Capacitor): 0.1µF ceramic**
   - Required per datasheet (between Pin 5 and Pin 8)
   - Filters high-frequency noise

4. **C2 (Bulk Capacitor): 10-100µF electrolytic**
   - On DC isolator output
   - Provides stable power during switching
   - Smooths voltage ripple

### DC Isolator Input

5. **C3 (Input Filter): 0.1µF ceramic**
   - Filters noise from USB power

## Step-by-Step Wiring

### Input Side (Feather Connection):
1. Connect GPIO Pin 6 (D4) to one end of the 220Ω resistor
2. Connect other end of resistor to **Pin 2** of HCPL-2211 (Anode)
3. Connect **Pin 3** of HCPL-2211 (Cathode) to Feather GND

### Output Side (Isolated TTL):
1. Connect DC isolator positive output to **Pin 8** (VCC)
2. Connect DC isolator negative output to **Pin 5** (GND)
3. Connect 0.1µF ceramic capacitor between Pin 5 and Pin 8
4. Connect 10µF electrolytic capacitor across DC isolator output (+ to +, - to -)
5. Connect **Pin 7** (VO) to one end of 47Ω resistor
6. Connect other end of 47Ω resistor to BNC center pin (+)
7. Connect **Pin 5** (GND) to BNC shield (-)
8. Leave Pin 6 unconnected (NC)

### DC Isolator Input:
1. Connect USB 5V to DC isolator input positive
2. Connect Feather GND to DC isolator input negative
3. Add 0.1µF ceramic capacitor across input

## Signal Behavior

### Truth Table (Non-Inverting)
| GPIO State | LED State | Output (VO) |
|------------|-----------|-------------|
| LOW        | OFF       | LOW (~0.3V) |
| HIGH       | ON        | HIGH (~3.9V)|

### Firmware Logic (OFF-to-ON pulses)
- **Idle**: GPIO LOW → LED OFF → Output LOW (~280mV)
- **Pulse**: GPIO HIGH → LED ON → Output HIGH (~3.9V)

### Timing
- Propagation delay: ~150-300ns typical
- Rise/fall time: ~30ns / ~7ns typical
- Suitable for scientific timing (<1ms latency requirement)

## Important Notes

### Isolation
- The optocoupler provides electrical isolation between the Feather and your TTL device
- Keep grounds separate: Feather GND ≠ DC Isolator output GND
- This protects both devices from ground loops and voltage spikes

### Power Requirements
- Input side: Powered by Feather (3.3V logic)
- Output side: Requires isolated 5V supply (DC isolator)
- Output current: Totem pole can source/sink ~25mA

### No Pull-up Resistor Needed
- The HCPL-2211 has a totem pole (push-pull) output
- It actively drives both HIGH and LOW states
- Do NOT add a pull-up resistor

### Output Voltage
- VOH ≈ VCC - 0.3V (with totem pole)
- With 4.1V supply: expect ~3.8-3.9V output
- This is valid TTL level (>2.0V = HIGH)

## Troubleshooting

**No output signal:**
- Verify DC isolator is providing power to Pin 8
- Check 0.1µF bypass capacitor is installed
- Confirm LED is conducting (measure ~1.4V at Pin 2 relative to Pin 3)

**Output stuck HIGH:**
- Check GPIO is actually going LOW at idle
- Verify Pin 3 (Cathode) connects to Feather GND, not Pin 2

**Output stuck LOW:**
- Check DC isolator output voltage (should be 4-5V)
- Verify Pin 2 (Anode) receives the resistor, not Pin 1 or Pin 3

**Weak or noisy signal:**
- Add/verify 10µF electrolytic on DC isolator output
- Check all ground connections are solid

## Parts List

| Component | Value | Quantity | Notes |
|-----------|-------|----------|-------|
| HCPL-2211 | - | 1 | DIP-8 optocoupler |
| Resistor | 220Ω | 1 | 1/4W, input current limiting |
| Resistor | 47Ω | 1 | 1/4W, output impedance matching |
| Capacitor | 0.1µF ceramic | 2 | Bypass/filter |
| Capacitor | 10µF electrolytic | 1 | 10V+ rating, bulk filter |
| DC Isolator | 5V isolated | 1 | e.g., B0505S-1W or similar |
| BNC Connector | - | 1 | Panel mount or cable |
