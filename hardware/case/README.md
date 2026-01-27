# HyperStudy TTL Case

3D printable enclosure for the HyperStudy TTL FeatherWing + Adafruit Feather RP2040 stack.

## Files

| File | Description |
|------|-------------|
| `hyperstudy-ttl-case.scad` | OpenSCAD parametric design source |
| `hyperstudy_icon.svg` | HyperStudy logo for embossing |
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
| Walls | 4 perimeters | Strength at screw bosses |
| Top/Bottom | 5 layers | Prevents lid flex |
| Infill | 15% gyroid | Good strength-to-weight |
| Supports | Not required | Designed for supportless printing |
| Brim | 5mm (first print) | Helps bed adhesion |
| Orientation | Print flat (opening facing up) | Critical for quality |

### Print Time (Bambu P1/X1 estimated)
- Bottom shell: ~45min - 1 hour
- Top shell: ~1 - 1.5 hours

## Hardware Required

| Item | Quantity | Notes |
|------|----------|-------|
| M3 x 12mm screws | 4 | Pan head or countersunk |
| Rubber feet | 4 | ~10mm diameter adhesive feet |

## Assembly

1. **Prepare the PCB stack**
   - Solder all components to FeatherWing
   - Stack FeatherWing onto Feather RP2040 via headers

2. **Install in bottom shell**
   - Place assembled PCB stack into bottom shell
   - Feather RP2040 should rest on the mounting standoffs
   - USB port aligns with cutout on short end

3. **Attach top shell**
   - Place top shell over assembly
   - BNC connector should protrude through cutout
   - Align screw holes at corners

4. **Secure with screws**
   - Insert M3 screws through top shell
   - Thread into screw bosses in bottom shell
   - Tighten snugly (don't overtighten)

5. **Add rubber feet**
   - Apply adhesive rubber feet to recesses on bottom

## Customization

The OpenSCAD file is fully parametric. Adjust parameters in the Customizer or by editing values:

```scad
/* Key parameters to adjust */
pcb_clearance = 0.5;      // Increase if fit is too tight
wall = 2.5;               // Wall thickness
component_height_top = 15; // Increase if components don't fit
```

## Dimensions

| Dimension | Value |
|-----------|-------|
| Case length | ~99mm (including BNC) |
| Case width | ~33mm |
| Case height | ~38mm (assembled) |
| PCB cutout | 78.8mm x 27.7mm |

## Troubleshooting

**PCB doesn't fit:**
- Increase `pcb_clearance` parameter (default 0.5mm)
- Check for print artifacts on ledges
- Verify first layer isn't squished (elephant foot)

**BNC doesn't align:**
- Adjust `bnc_extension` parameter
- Modify `bnc_diameter` for your specific connector (default 10.2mm for panel-mount)

**USB port blocked:**
- Adjust `usb_width`, `usb_height`, or `usb_offset_y`
- Increase `usb_corner_radius` if corners are rough

**Logo not rendering:**
- Ensure `hyperstudy_icon.svg` is in same directory
- Check OpenSCAD console for import errors

## Tolerance Debugging Checklist

Use this checklist when test-fitting your first print:

### Fit Issues
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| PCB won't seat flat | Standoffs too tall | Reduce `standoff_height` by 0.2-0.3mm |
| PCB rocks/wobbles | Standoffs uneven | Check print bed level, re-slice |
| Shells don't close | Screw bosses too long | Reduce `screw_boss_height` |
| USB cable won't insert | Cutout too small | Increase `usb_width` to 10.5mm |
| BNC nut won't seat | Hole too small | Increase `bnc_diameter` to 10.5mm |

### Print Quality Issues
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Stringing at connectors | Travel speed too low | Increase retraction, enable wipe |
| Layer separation at walls | Under-extrusion | Increase flow 2-5%, check nozzle |
| Warped corners | Bed adhesion | Add brim, increase bed temp |
| Rough USB cutout | Sharp corners | `usb_corner_radius` should be ≥0.6mm |

### Measurement Tips
1. **Calipers required** - Don't eyeball tolerances
2. **Measure printed parts** - Actual dimensions often differ from CAD by ±0.2mm
3. **Test fit components first** - Before final assembly, dry-fit PCB and connectors
4. **Room for adjustment** - If holes are slightly tight, a 3mm drill bit can clean them up
