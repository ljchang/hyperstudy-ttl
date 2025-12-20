# HyperStudy TTL FeatherWing Schematic

This document describes the schematic design for a FeatherWing add-on board that provides electrically-isolated TTL output from an Adafruit Feather RP2040.

## Design Overview

The FeatherWing provides:
- HCPL-2211 optocoupler for galvanic isolation
- Isolated 5V power supply (B0505S-1W DC-DC isolator)
- BNC output connector for TTL signal
- All necessary bypass capacitors and current limiting resistors

## Schematic Block Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HyperStudy TTL FeatherWing                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Feather                                                                   │
│   Header         Input Stage           Isolation          Output Stage     │
│                                                                             │
│   D4 (GP6) ──────[220Ω]──────┐                                             │
│                               │      HCPL-2211                              │
│                               ├─────┤2 (A)  8├───────────┬──── +5V ISO     │
│                               │     │        │           │                  │
│   GND ────────────────────────┴─────┤3 (K)  7├──[47Ω]────┼───► BNC+        │
│                                     │        │           │                  │
│                              NC ────┤1      6├── NC      │                  │
│                                     │        │           │                  │
│                              NC ────┤4      5├───────────┼──── GND ISO     │
│                                     └────────┘           │      │          │
│                                                   [0.1µF]│    [BNC-]       │
│                                                          │                  │
│                                                          └──────────────────┤
│   USB 5V ─────┬─────[0.1µF]─────┬─────────────────────────────────────────┤
│               │                 │         B0505S-1W                        │
│               │                 │        ┌─────────┐                       │
│               └─────────────────┼────────┤+Vin Vout+├───────► +5V ISO     │
│                                 │        │         │                       │
│   GND ──────────────────────────┼────────┤-Vin Vout-├───────► GND ISO     │
│                                 │        └─────────┘     │                 │
│                              [10µF]                   [10µF]               │
│                                 │                        │                 │
│                                GND                    GND ISO              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component List

### Semiconductors
| Ref | Component | Value | Package | Notes |
|-----|-----------|-------|---------|-------|
| U1 | HCPL-2211 | - | DIP-8 | Totem pole optocoupler |
| U2 | B0505S-1W | 5V→5V | SIP-4 | 1W isolated DC-DC converter |

### Resistors
| Ref | Value | Package | Tolerance | Notes |
|-----|-------|---------|-----------|-------|
| R1 | 220Ω | 0805 | 5% | LED current limiting (8mA) |
| R2 | 47Ω | 0805 | 5% | BNC impedance matching |

### Capacitors
| Ref | Value | Package | Voltage | Notes |
|-----|-------|---------|---------|-------|
| C1 | 0.1µF | 0805 | 16V | DC isolator input filter |
| C2 | 10µF | Electrolytic | 16V | DC isolator input bulk |
| C3 | 0.1µF | 0805 | 16V | Optocoupler bypass (Pin 5-8) |
| C4 | 10µF | Electrolytic | 16V | Optocoupler output bulk |

### Connectors
| Ref | Component | Notes |
|-----|-----------|-------|
| J1 | Feather Header (16-pin) | Left side of Feather |
| J2 | Feather Header (12-pin) | Right side of Feather |
| J3 | BNC Female | Panel mount or PCB mount |

## Feather Header Pinout (Relevant Pins)

### Left Header (J1 - 16 pins, top to bottom)
```
Pin  Name    Use
1    RST     -
2    3V3     -
3    AREF    -
4    GND     Optocoupler cathode (Pin 3)
5    A0      -
6    A1      -
7    A2      -
8    A3      -
9    24      -
10   25      -
11   SCK     -
12   MOSI    -
13   MISO    -
14   RX      -
15   TX      -
16   D4      → TTL Trigger (GP6)
```

### Right Header (J2 - 12 pins, top to bottom)
```
Pin  Name    Use
1    VBAT    -
2    EN      -
3    VBUS    USB 5V → DC isolator input
4    D13     -
5    D12     -
6    D11     -
7    D10     -
8    D9      -
9    D6      -
10   D5      -
11   SCL     -
12   SDA     -
```

## Schematic Connections

### Input Stage (Non-Isolated)
1. **D4 (GP6)** → R1 (220Ω) → U1 Pin 2 (Anode)
2. **GND** → U1 Pin 3 (Cathode)
3. **VBUS** → C1 (0.1µF) → GND
4. **VBUS** → C2 (10µF +) → GND
5. **VBUS** → U2 Pin 1 (+Vin)
6. **GND** → U2 Pin 2 (-Vin)

### Output Stage (Isolated)
1. **U2 Pin 4 (+Vout)** → U1 Pin 8 (VCC)
2. **U2 Pin 3 (-Vout)** → U1 Pin 5 (GND)
3. **U1 Pin 5** → C3 (0.1µF) → U1 Pin 8
4. **U1 Pin 5** → C4 (10µF -), C4 (+) → U1 Pin 8
5. **U1 Pin 7 (VO)** → R2 (47Ω) → J3 BNC Center
6. **U1 Pin 5 (GND)** → J3 BNC Shield
7. **U1 Pin 1, 4, 6** → NC (No Connection)

## Design Notes

### Isolation Barrier
- The dashed line in the block diagram represents the isolation barrier
- Input ground (Feather GND) and output ground (ISO GND) must be kept separate
- The B0505S-1W provides 1kV isolation between input and output

### Component Placement
- Place C3 (bypass cap) as close to U1 pins 5 and 8 as possible
- Keep the input stage components grouped on one side of the board
- Keep the output stage components grouped on the other side
- Maintain creepage distance across isolation barrier (min 2mm recommended)

### Totem Pole Output
- The HCPL-2211 has an active push-pull output
- No pull-up resistor is needed
- Output can source/sink ~25mA

### Signal Integrity
- R2 (47Ω) provides approximate 50Ω impedance matching for BNC cable
- Keep traces to BNC connector short and direct

## EasyEDA Import Instructions

1. Open EasyEDA (https://easyeda.com)
2. Create a new project: File → New → Project
3. Create a new schematic: File → New → Schematic
4. Import components from LCSC (EasyEDA's parts library):
   - Search for each component by part number
   - Add to schematic
5. Wire components according to the connections above
6. Convert to PCB: Design → Convert to PCB
7. Arrange components on the PCB
8. Route traces (auto-route or manual)
9. Add ground planes if desired
10. Run DRC (Design Rule Check)
11. Generate Gerber files for fabrication

## Bill of Materials (BOM)

| Qty | Component | Value | LCSC Part # | Notes |
|-----|-----------|-------|-------------|-------|
| 1 | HCPL-2211 | - | C6933 | DIP-8 optocoupler |
| 1 | B0505S-1W | 5V | C87025 | DC-DC isolator |
| 1 | Resistor | 220Ω | C17557 | 0805, 5% |
| 1 | Resistor | 47Ω | C17714 | 0805, 5% |
| 2 | Capacitor | 0.1µF | C49678 | 0805 ceramic |
| 2 | Capacitor | 10µF | C19702 | Electrolytic 16V |
| 1 | BNC Connector | Female | C496553 | PCB mount |
| 1 | Pin Header | 1x16 2.54mm | C2337 | Female for Feather |
| 1 | Pin Header | 1x12 2.54mm | C2334 | Female for Feather |

Note: LCSC part numbers are examples. Verify availability and specifications before ordering.

## FeatherWing Dimensions

Standard FeatherWing dimensions:
- Width: 22.86mm (0.9")
- Length: 50.8mm (2.0")
- Mounting holes: Match Feather pattern

The BNC connector will extend beyond the standard FeatherWing footprint.
Consider using a right-angle BNC or panel-mount BNC with wires.

## Testing After Assembly

1. Power on with Feather RP2040 attached
2. Measure isolated 5V output (should read 4.1-5.0V)
3. Connect multimeter to BNC output
4. Idle voltage should be ~0.3V (LOW)
5. Send PULSE command via serial
6. Pulse voltage should reach ~3.9V (HIGH)
