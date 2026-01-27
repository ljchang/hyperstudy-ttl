// HyperStudy TTL FeatherWing Case
// Parametric design for 3D printing
//
// Usage:
//   - Render bottom_shell() and export as bottom.stl
//   - Render top_shell() and export as top.stl
//   - Print orientation (IMPORTANT):
//       * Bottom shell: Print as exported (floor on bed)
//       * Top shell: FLIP UPSIDE DOWN in slicer (ceiling on bed, open side up)
//   - Insert M2 nuts into hex pockets on bottom shell exterior
//   - Assemble with 4x M2 screws (~25-30mm) through top shell, PCB, standoffs, into nuts

/* [PCB Dimensions] */
// FeatherWing v1.1 PCB length (mm)
pcb_length = 81.30;
// FeatherWing v1.1 PCB width (mm)
pcb_width = 34.80;
// PCB thickness (mm)
pcb_thickness = 1.6;
// BNC connector extension past board edge (mm) - set to 0 so BNC protrudes outside case
bnc_extension = 0;
// Feather overhang past FeatherWing on USB end (mm)
feather_extension = 5;

/* [Component Heights] */
// Height above FeatherWing PCB for Feather RP2040 + headers (measured: 19.6mm to top)
component_height_top = 19.6;
// Height below FeatherWing PCB for BNC/solder joints (measured: 4.75mm lowest point)
component_height_bottom = 5;

/* [Case Parameters] */
// Wall thickness (mm)
wall = 2.5;
// Floor/ceiling thickness (mm) - 4mm to accommodate M2 nut pockets (2mm) with 2mm solid above
floor_thickness = 4;
// PCB clearance on each side (mm) - increased to accommodate support ribs
pcb_clearance = 1.5;
// Corner radius (mm)
corner_radius = 3;
// External edge chamfer for clean printing (mm)
edge_chamfer = 0.8;

/* [Screw Parameters] */
// M2 screw clearance hole diameter (mm)
screw_hole_diameter = 2.2;
// M2 nut width across flats (mm) - actual is 4.0mm, add 0.5mm tolerance
nut_width = 4.5;
// M2 nut pocket depth (mm) - actual nut is 1.6mm thick
nut_pocket_depth = 2.0;

/* [Connector Cutouts] */
// USB-C port width (mm)
usb_width = 10;
// USB-C port height (mm)
usb_height = 4;
// USB-C corner radius for printability and aesthetics (mm)
usb_corner_radius = 1.5;
// USB port vertical offset from shell interface (mm) - adjusted +4.2mm from original calibration
usb_offset_z = 14.05;
// USB port horizontal offset from center (mm)
usb_offset_y = 0;
// BNC connector diameter (mm) - panel-mount requires ~12.5mm clearance (+0.5mm tolerance)
bnc_diameter = 13;
// BNC connector vertical offset from shell interface (mm) - positive moves hole up
bnc_offset_z = 2.65;

/* [Rubber Feet] */
// Rubber foot recess diameter (mm)
foot_diameter = 10;
// Rubber foot recess depth (mm) - reduced to preserve floor strength
foot_depth = 1;
// Foot offset toward center (mm) - moves feet away from case edges while still covering nuts
// Max ~1.5mm with 10mm foot and 5.2mm nut pocket
foot_center_offset = 1.5;

/* [PCB Support Ribs] */
// Enable PCB edge support ribs in top shell
pcb_supports_enabled = true;
// Rib thickness (mm) - how far rib extends from wall toward PCB (must be < pcb_clearance)
pcb_support_width = 1.2;
// Rib height from open edge (mm) - should reach beside PCB edge
pcb_support_height = 5;
// Gap between rib and PCB edge (mm) - clearance = pcb_clearance - pcb_support_width
// Current: 1.5 - 1.2 = 0.3mm gap

// Rail positioning - runs along Feather section only (avoids FeatherWing components)
// Start after USB-side screw holes, run along where Feather sits
pcb_rail_start = 12;              // Start X position (mm from USB end wall, after screw holes)
pcb_rail_length = 32;             // Length of rail (mm) - covers Feather area
// Z offset = PCB thickness + clearance, so rails are above PCB when it sits flush/inset
pcb_rail_z_offset = pcb_thickness + 0.5;  // 1.6 + 0.5 = 2.1mm from open edge

// BNC-side corner posts (between BNC cutout and screw holes)
bnc_posts_enabled = true;
bnc_post_diameter = 4;            // Post diameter (mm)
bnc_post_height = 4;              // Post height (mm)
bnc_post_inset_x = 5;             // Post X inset from BNC end wall (mm)
bnc_post_inset_y = 10;            // Post Y inset from case side walls (mm)

/* [Logo] */
// Logo scale factor (0.07 = large, may extend to edges)
logo_scale = 0.07;
// Logo emboss depth (mm)
logo_depth = 0.8;
// Logo X offset from center (mm)
logo_offset_x = 0;
// Logo Y offset from center (mm)
logo_offset_y = 22;
// Logo rotation (degrees)
logo_rotation = 90;

/* [Rendering] */
// Resolution for curved surfaces
$fn = 50;

// Calculated dimensions
case_inner_length = pcb_length + 2 * pcb_clearance + feather_extension;
case_inner_width = pcb_width + 2 * pcb_clearance;
case_outer_length = case_inner_length + 2 * wall;
case_outer_width = case_inner_width + 2 * wall;
case_height_bottom = component_height_bottom + floor_thickness;
case_height_top = component_height_top + wall + pcb_thickness;
total_case_length = case_outer_length + bnc_extension;

// PCB ledge parameters
pcb_ledge_height = 2;
pcb_ledge_width = 1.5;

// FeatherWing v1.1 mounting hole positions (from PCB corner)
// 4x M2 mounting holes extracted from Gerber drill file
fw_hole_inset_x = 2.54;           // Hole inset from left/right edges
fw_hole_inset_y = 2.54;           // Hole inset from bottom/top edges
fw_hole_spacing_x = 76.2;         // Horizontal spacing between holes
fw_hole_spacing_y = 29.72;        // Vertical spacing between holes
fw_hole_diameter = 2.032;         // M2 clearance holes in PCB

// Standoff parameters (sized for M2 screws)
standoff_diameter = 5;
standoff_hole_diameter = 2.2;     // M2 clearance hole (screw passes through to nut below)
standoff_height = component_height_bottom + 0.3;  // Height to support PCB (+0.3mm margin so PCB doesn't rub lid)
pcb_bnc_offset = 0.8;             // Extra clearance between PCB/standoffs and BNC end (mm)

// Module: Rounded box with optional edge chamfer
module rounded_box(length, width, height, radius, chamfer = 0) {
    if (chamfer > 0) {
        // Box with chamfered top edge for clean printing
        hull() {
            for (x = [radius, length - radius]) {
                for (y = [radius, width - radius]) {
                    translate([x, y, 0])
                        cylinder(r = radius, h = height - chamfer);
                    translate([x, y, height - chamfer])
                        cylinder(r1 = radius, r2 = radius - chamfer, h = chamfer);
                }
            }
        }
    } else {
        // Simple rounded box without chamfer
        hull() {
            for (x = [radius, length - radius]) {
                for (y = [radius, width - radius]) {
                    translate([x, y, 0])
                        cylinder(r = radius, h = height);
                }
            }
        }
    }
}

// Module: Rounded rectangle for USB-C cutout (extruded along X axis)
// Creates a rounded rectangle in the Y-Z plane, extruded along X
module rounded_rect(width, height, depth, radius) {
    translate([0, radius, radius])
    hull() {
        for (y = [0, width - 2*radius])
            for (z = [0, height - 2*radius])
                translate([0, y, z])
                    rotate([0, 90, 0])
                        cylinder(r = radius, h = depth);
    }
}

// Module: Bottom shell
module bottom_shell() {
    difference() {
        // Main body with chamfered bottom edge (prints on bed)
        rounded_box(total_case_length, case_outer_width, case_height_bottom, corner_radius, edge_chamfer);

        // Inner cavity
        translate([wall, wall, floor_thickness])
            rounded_box(case_inner_length + bnc_extension, case_inner_width,
                       case_height_bottom, corner_radius - wall/2);

        // Rubber feet recesses
        for (pos = foot_positions()) {
            translate([pos[0], pos[1], -0.1])
                cylinder(d = foot_diameter, h = foot_depth + 0.1);
        }

        // M2 hex nut pockets on exterior bottom (beneath standoffs)
        // Hex pocket holds nut while screw tightens from top
        for (pos = standoff_positions()) {
            // Clearance hole through floor
            translate([pos[0], pos[1], -0.1])
                cylinder(d = screw_hole_diameter, h = floor_thickness + 0.2);
            // Hex nut pocket (rotate 30° so flat sides align with case edges)
            translate([pos[0], pos[1], -0.1])
                rotate([0, 0, 30])
                    cylinder(d = nut_width / cos(30), h = nut_pocket_depth + 0.1, $fn = 6);
        }

        // BNC connector cutout (offset from shell interface)
        translate([total_case_length - wall - 1, case_outer_width/2, case_height_bottom + bnc_offset_z])
            rotate([0, 90, 0])
                cylinder(d = bnc_diameter, h = wall + 2);
    }

    // FeatherWing v1.1 mounting standoffs (at PCB mounting holes)
    // Positioned to align with the 4 corner mounting holes on the FeatherWing
    // Offset by feather_extension to leave room for Feather overhang at USB end
    // pcb_bnc_offset shifts PCB away from BNC wall for clearance
    for (dx = [fw_hole_inset_x, fw_hole_inset_x + fw_hole_spacing_x]) {
        for (dy = [fw_hole_inset_y, fw_hole_inset_y + fw_hole_spacing_y]) {
            translate([wall + pcb_clearance + feather_extension + dx - pcb_bnc_offset,
                       wall + pcb_clearance + dy,
                       floor_thickness]) {
                difference() {
                    cylinder(d = standoff_diameter, h = standoff_height);
                    translate([0, 0, -0.1])
                        cylinder(d = standoff_hole_diameter, h = standoff_height + 0.2);
                }
            }
        }
    }
}

// Module: Top shell
module top_shell() {
    union() {
        difference() {
            // Main body with chamfered top edge for clean printing
            rounded_box(total_case_length, case_outer_width, case_height_top, corner_radius, edge_chamfer);

        // Inner cavity
        translate([wall, wall, -0.1])
            rounded_box(case_inner_length + bnc_extension, case_inner_width,
                       case_height_top - wall + 0.1, corner_radius - wall/2);

        // USB-C port cutout with rounded corners (sharp corners crack when printing)
        // usb_offset_z is measured from PCB bottom surface
        translate([-1, case_outer_width/2 - usb_width/2 + usb_offset_y,
                   usb_offset_z])
            rounded_rect(usb_width, usb_height, wall + 2, usb_corner_radius);

        // BNC connector cutout (offset to align with bottom shell)
        translate([total_case_length - wall - 1, case_outer_width/2, bnc_offset_z])
            rotate([0, 90, 0])
                cylinder(d = bnc_diameter, h = wall + 2);

        // M2 screw holes (aligned with standoffs/PCB mounting holes)
        for (pos = standoff_positions()) {
            translate([pos[0], pos[1], case_height_top - wall - 0.1])
                cylinder(d = screw_hole_diameter, h = wall + 0.2);
            // Countersink for M2 screw head
            translate([pos[0], pos[1], case_height_top - 1.5])
                cylinder(d1 = screw_hole_diameter, d2 = screw_hole_diameter + 2, h = 1.6);
        }

        // Logo emboss (debossed into top surface) - DISABLED until case design finalized
        /*
        translate([case_outer_length/2 + logo_offset_x,
                   case_outer_width/2 + logo_offset_y,
                   case_height_top - logo_depth])
            linear_extrude(height = logo_depth + 0.1)
                rotate([0, 0, logo_rotation])
                    scale([logo_scale, logo_scale, 1])
                        translate([-512, -512, 0])  // Center the 1024x1024 viewBox
                            import("hyperstudy_icon.svg", center = false);
        */
        } // end difference

        // PCB support ribs (added after cavity subtraction so they extend into interior)
        // Rails along Feather section only - avoids FeatherWing components
        // Z offset allows PCB to sit flush or slightly inset at the open edge
        if (pcb_supports_enabled) {
            // Left rib (low Y side) - extends from wall into cavity
            translate([pcb_rail_start, wall - 1, pcb_rail_z_offset])
                cube([pcb_rail_length,
                      pcb_support_width + 1,
                      pcb_support_height]);
            // Right rib (high Y side) - extends from wall into cavity
            translate([pcb_rail_start,
                      case_outer_width - wall - pcb_support_width, pcb_rail_z_offset])
                cube([pcb_rail_length,
                      pcb_support_width + 1,
                      pcb_support_height]);
        }

        // BNC-side support ribs (between BNC cutout and screw holes)
        // Extend from BNC wall to ceiling for solid connection
        if (bnc_posts_enabled) {
            // Rib near low Y side - connects wall to ceiling
            translate([total_case_length - wall - bnc_post_inset_x,
                      bnc_post_inset_y - bnc_post_diameter/2,
                      pcb_rail_z_offset])
                cube([bnc_post_inset_x + 1,  // +1 to merge with wall
                      bnc_post_diameter,
                      case_height_top - wall - pcb_rail_z_offset]);
            // Rib near high Y side - connects wall to ceiling
            translate([total_case_length - wall - bnc_post_inset_x,
                      case_outer_width - bnc_post_inset_y - bnc_post_diameter/2,
                      pcb_rail_z_offset])
                cube([bnc_post_inset_x + 1,  // +1 to merge with wall
                      bnc_post_diameter,
                      case_height_top - wall - pcb_rail_z_offset]);
        }
    } // end union
}

// Function: Standoff/screw positions (aligned with FeatherWing mounting holes)
// These positions are used for both the PCB standoffs and the shell assembly screws
function standoff_positions() = [
    for (dx = [fw_hole_inset_x, fw_hole_inset_x + fw_hole_spacing_x])
        for (dy = [fw_hole_inset_y, fw_hole_inset_y + fw_hole_spacing_y])
            [wall + pcb_clearance + feather_extension + dx - pcb_bnc_offset,
             wall + pcb_clearance + dy]
];

// Function: Rubber foot positions (offset toward center from standoffs, still covering nut pockets)
function foot_positions() = [
    for (pos = standoff_positions())
        [pos[0] + (pos[0] < total_case_length/2 ? foot_center_offset : -foot_center_offset),
         pos[1] + (pos[1] < case_outer_width/2 ? foot_center_offset : -foot_center_offset)]
];

// Render selection - uncomment one to export
// For bottom.stl:
// bottom_shell();

// For top.stl:
// top_shell();

// Assembly view (for visualization)
color("DarkSlateGray") bottom_shell();
translate([0, 0, case_height_bottom + 2])
    color("SlateGray") top_shell();

// PCB placeholder (for visualization only)
// translate([wall + pcb_clearance, wall + pcb_clearance, case_height_bottom])
//     color("Green", 0.5) cube([pcb_length, pcb_width, pcb_thickness]);
