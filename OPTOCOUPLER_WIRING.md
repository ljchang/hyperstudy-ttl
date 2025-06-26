# HCPL-2211 Optocoupler Wiring Guide

## Circuit Diagram

```
Feather RP2040 Side                     Isolated Output Side
                                        
                    HCPL-2211
                   ┌─────────┐
GPIO 5 ──[220Ω]───┤1 (A)  8 ├─── +5V (External)
                   │         │
Feather GND ───────┤2 (K)  7 ├─── TTL Output ──┬──[10kΩ]── +5V
                   │         │                  │
        NC ────────┤3      6 ├─── +5V (Enable) │
                   │         │                  │
        NC ────────┤4      5 ├─── GND (External)
                   └─────────┘

Legend:
- A = Anode (LED +)
- K = Cathode (LED -)
- [220Ω] = Current limiting resistor
- [10kΩ] = Pull-up resistor
```

## Component Values

1. **R1 (LED Current Limiting)**: 220Ω
   - Calculation: (3.3V - 1.4V) / 8mA ≈ 237Ω → Use 220Ω standard value
   - Ensures safe current for internal LED

2. **R2 (Output Pull-up)**: 10kΩ
   - Provides clean HIGH signal when output is off
   - Can be adjusted based on load requirements

## Step-by-Step Wiring

### Input Side (Feather Connection):
1. Connect GPIO Pin 5 to one end of the 220Ω resistor
2. Connect other end of resistor to Pin 1 of HCPL-2211
3. Connect Pin 2 of HCPL-2211 to Feather GND

### Output Side (Isolated TTL):
1. Connect Pin 8 to external +5V supply
2. Connect Pin 6 to external +5V supply (this enables the output)
3. Connect Pin 7 to one end of 10kΩ resistor
4. Connect other end of 10kΩ resistor to external +5V
5. Connect Pin 5 to external ground (NOT Feather ground)
6. Pin 7 is your TTL output signal

## Important Notes

### Isolation
- The optocoupler provides electrical isolation between the Feather and your TTL device
- Keep grounds separate - do NOT connect Feather GND to external GND
- This protects both devices from ground loops and voltage spikes

### Power Requirements
- Input side: Powered by Feather (3.3V logic)
- Output side: Requires separate 5V supply
- Current consumption: ~10mA input, ~20mA output max

### Signal Characteristics
- When GPIO 5 is HIGH: TTL output goes LOW (inverted)
- When GPIO 5 is LOW: TTL output goes HIGH (via pull-up)
- Rise/fall time: ~3μs typical
- Maximum frequency: ~100kHz

### Testing
1. Before connecting to your equipment, test with a multimeter
2. You should see ~5V on the output when GPIO 5 is LOW
3. You should see ~0V on the output when GPIO 5 is HIGH

## Troubleshooting

**No output signal:**
- Check +5V supply is connected to pins 6 and 8
- Verify 220Ω resistor is connected
- Ensure grounds are properly isolated

**Weak or slow signal:**
- Reduce pull-up resistor value (try 4.7kΩ)
- Check your 5V supply can provide adequate current
- Verify connections are solid

**Inverted signal:**
If your equipment expects non-inverted signals, you can:
1. Invert in software (change HIGH/LOW in firmware)
2. Add a transistor inverter on the output
3. Use a non-inverting optocoupler like HCPL-2631