// Test 2.5 — VTI medium, oblique fault (45° to VTI symmetry axis).
//
// Geometry:  10 × 10 × 5 km box; the fault is a planar surface whose
//            normal n = (0, sin(45°), -cos(45°)) lies at 45° to z-axis.
//            We construct the fault as a 6 × 3 km rectangle in the
//            global frame, embedded in the volume.
//
// Purpose:  The Christoffel matrix is now full 3×3 in fault-local
//           (n,s,d) coordinates: off-diagonals Z_ns and Z_sd are non-zero.
//           Tests the full matrix path and the slip-direction projection.

lc        = 4000;
lc_fault  = 400;

theta     = Pi / 4;       // 45-degree dip from horizontal
ct        = Cos(theta);
st        = Sin(theta);

Fault_strike_len = 6000;  // along strike (x)
Fault_dip_len    = 3000;  // along dip

Xmin = -5000;  Xmax =  5000;
Ymin = -5000;  Ymax =  5000;
Ztop =     0;  Zbot = -5000;

// ---------- top (free surface) ---------------------------------------
Point(1) = {Xmin, Ymin, Ztop, lc};
Point(2) = {Xmin, Ymax, Ztop, lc};
Point(3) = {Xmax, Ymax, Ztop, lc};
Point(4) = {Xmax, Ymin, Ztop, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Curve Loop(5) = {1, 2, 3, 4};
Plane Surface(1) = {5};
Extrude {0, 0, Zbot} { Surface{1}; }

// ---------- fault rectangle  -----------------------------------------
// Strike axis = x. Dip axis = (0, ct, -st) so the fault normal is
// n = (0, st, ct) — 45° from vertical, leaning northward.
// Top edge of fault at z=0, slipping into +y, -z.
xL = -0.5 * Fault_strike_len;
xR =  0.5 * Fault_strike_len;

// upper edge (free-surface intersection): z = 0, y = 0
Point(100) = {xL, 0, 0, lc_fault};
Point(101) = {xR, 0, 0, lc_fault};

// lower edge: shifted by Fault_dip_len along (0, ct, -st)
y_low =  Fault_dip_len * ct;
z_low = -Fault_dip_len * st;
Point(102) = {xR, y_low, z_low, lc_fault};
Point(103) = {xL, y_low, z_low, lc_fault};

Line(100) = {100, 101};
Line(101) = {101, 102};
Line(102) = {102, 103};
Line(103) = {103, 100};
Line{100} In Surface{1};
Curve Loop(104) = {100, 101, 102, 103};
Plane Surface(100) = {104};
Surface{100} In Volume{1};

// ---------- mesh size field ------------------------------------------
Field[1] = Distance;
Field[1].FacesList = {100};
Field[2] = MathEval;
Field[2].F = Sprintf("0.05*F1 + (F1/2.5e3)^2 + %g", lc_fault);
Background Field = 2;

// ---------- physical groups ------------------------------------------
Physical Surface(101) = {1};
Physical Surface(103) = {100};
Physical Surface(105) = {14, 18, 22, 26, 27};
Physical Volume(1)    = {1};

Mesh.MshFileVersion = 2.2;
