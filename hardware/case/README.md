# HyperStudy TTL Case

3D printable enclosure for the HyperStudy TTL FeatherWing + Adafruit Feather RP2040 stack.

## Files

| File | Description |
|------|-------------|
| `hyperstudy-ttl-case.scad` | OpenSCAD parametric design source |
| `bottom.stl` | Bottom shell (generate from OpenSCAD) |
| `top.stl` | Top shell (generate from OpenSCAD) |

## Generating STL Files

1. Install [OpenSCAD](https://openscad.org/downloads.html)
2. Open `hyperstudy-ttl-case.scad`
3. For bottom shell:
   - Comment out assembly view at bottom
   - Uncomment `bottom_shell();`
   - Render (F6) and Export as STL
4. For top shell:
   - Comment out `bottom_shell();`
   - Uncomment `top_shell();`
   - Render (F6) and Export as STL

## Printing Recommendations

### Material
- **PLA**: Easy to print, good for most uses
- **PETG**: Better heat resistance and durability
- **ABS**: Best durability, requires enclosure

### Settings (Bambu Studio / PrusaSlicer)
| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| Layer height | 0.20mm | 0.16mm for finer detail |
| Walls | 4 perimeters | Strength at screw holes |
| Top/Bottom | 5 layers | Prevents flex |
| Infill | 15% gyroid | Good strength-to-weight |
| Supports | Not required | Designed for supportless printing |
| Brim | 5mm (first print) | Helps bed adhesion |

### Print Orientation (Critical)
- **Bottom shell**: Print as exported (floor on print bed)
- **Top shell**: Flip upside down in slicer (ceiling on print bed, open side facing up)

### Print Time (Bambu P1/X1 estimated)
- Bottom shell: ~45min - 1 hour
- Top shell: ~1 - 1.5 hours

## Hardware Required

| Item | Quantity | Notes |
|------|----------|-------|
| M2 x 35mm pan head screws | 4 | Through top shell, PCB, standoffs |
| M2 hex nuts | 4 | Press into hex pockets on bottom exterior |
| Rubber feet (optional) | 4 | ~10mm diameter adhesive feet |

## Assembly

1. **Prepare the PCB stack**
   - Solder all components to FeatherWing
   - Stack FeatherWing onto Feather RP2040 via headers

2. **Install M2 nuts in bottom shell**
   - Press M2 hex nuts into the 4 hex pockets on the exterior bottom
   - Nuts should sit flush or slightly recessed

3. **Install PCB in bottom shell**
   - Place assembled PCB stack onto the 4 standoffs
   - PCB mounting holes align with standoff holes
   - USB port aligns with cutout on short end
   - BNC connector faces opposite end

4. **Attach top shell**
   - Place top shell over assembly
   - Interlocking lip on bottom shell fits inside top shell cavity (3 sides)
   - BNC connector protrudes through cutout
   - Screw holes align at all 4 corners

5. **Secure with screws**
   - Insert M2x35mm screws through counterbored holes in top shell
   - Screws pass through: top shell ceiling > PCB > standoffs > floor > nuts
   - Tighten snugly (don't overtighten - plastic threads)

6. **Add rubber feet (optional)**
   - Apply adhesive rubber feet to bottom exterior

## Design Features

### Interlocking Lip
The bottom shell has a 1.5mm tall lip that extends into the top shell on three sides (USB end and both long sides). The BNC end is open to accommodate the panel-mount connector. This provides:
- Lateral alignment between shells
- Prevents shifting during use
- 0.3mm clearance for FDM printing tolerances

### PCB Support
The top shell includes internal ribs that press down on the PCB edges, securing it in place when assembled.

## Customization

The OpenSCAD file is fully parametric. Key parameters to adjust:

```scad
/* Fit adjustments */
pcb_clearance = 1.5;          // Clearance around PCB edges (mm)
lip_clearance = 0.3;          // Gap between interlocking lip and top shell (mm)

/* Structural */
wall = 2.5;                   // Wall thickness (mm)
floor_thickness = 6;          // Bottom shell floor (mm)
ceiling_thickness = 3.5;      // Top shell ceiling (mm)

/* Component clearance */
component_height_top = 19.6;  // Height above PCB for Feather + headers (mm)
component_height_bottom = 5;  // Height below PCB for BNC/solder joints (mm)

/* Connector cutouts */
bnc_diameter = 13;            // BNC hole diameter (mm)
usb_width = 10;               // USB-C port width (mm)
usb_height = 4;               // USB-C port height (mm)
```

## Dimensions

| Dimension | Value |
|-----------|-------|
| Case length | ~93mm |
| Case width | ~43mm |
| Case height (assembled) | ~36mm |
| Bottom shell height | 11mm |
| Top shell height | 24.7mm |
| Wall thickness | 2.5mm |

## Troubleshooting

### Fit Issues
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| PCB won't seat flat | Standoffs too tall | Reduce `standoff_height` |
| Shells won't close | PCB sitting too high | Verify `standoff_height = component_height_bottom` |
| Top shell shifts laterally | Lip clearance too large | Reduce `lip_clearance` |
| Lip won't fit in top shell | Lip clearance too small | Increase `lip_clearance` to 0.4mm |
| USB cable won't insert | Cutout too small | Increase `usb_width` or `usb_height` |
| BNC nut won't thread | Hole too small | Increase `bnc_diameter` |

### Print Quality Issues
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Stringing at cutouts | Retraction settings | Increase retraction, enable wipe |
| Hex pockets too tight | FDM shrinkage | Increase `nut_width` parameter |
| Screw holes too tight | FDM shrinkage | Increase `screw_hole_diameter` |
| Warped corners | Bed adhesion | Add brim, increase bed temp |

### Measurement Tips
1. Use calipers - don't eyeball tolerances
2. Measure printed parts - actual dimensions often differ from CAD by +/-0.2mm
3. Test fit components before final assembly
4. If holes are slightly tight, an M2 drill bit can clean them up
