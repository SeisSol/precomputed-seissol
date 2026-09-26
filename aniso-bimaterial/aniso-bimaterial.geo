// Test 2.6 — Bimaterial fault: anisotropic plus side, isotropic minus side.
//
// Simplified topology: the *entire* y=0 face is the dynamic-rupture
// interface. Spatial localisation of the rupture is achieved by the
// stress and friction parameters set in fault.yaml (background outside
// |x|<3km, |z|<3km is sub-critical and never breaks). This keeps the
// gmsh topology trivial and avoids any internal-surface PLC issues.
//
// Two volumes share the y=0 face explicitly via re-used points/lines.

lc       = 4000;
lc_fault =  400;

XL = -5000;  XR =  5000;
YL = -5000;  YR =  5000;
ZB = -5000;  ZT =     0;

// Points on the shared y=0 plane
Point(1) = {XL, 0, ZB, lc_fault};
Point(2) = {XR, 0, ZB, lc_fault};
Point(3) = {XR, 0, ZT, lc_fault};
Point(4) = {XL, 0, ZT, lc_fault};

// Points on the y=YL face (minus side)
Point(5) = {XL, YL, ZB, lc};
Point(6) = {XR, YL, ZB, lc};
Point(7) = {XR, YL, ZT, lc};
Point(8) = {XL, YL, ZT, lc};

// Points on the y=YR face (plus side)
Point(9)  = {XL, YR, ZB, lc};
Point(10) = {XR, YR, ZB, lc};
Point(11) = {XR, YR, ZT, lc};
Point(12) = {XL, YR, ZT, lc};

// y=0 shared face
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

// MINUS volume edges
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 5};
Line(9)  = {1, 5};
Line(10) = {2, 6};
Line(11) = {3, 7};
Line(12) = {4, 8};

Curve Loop(2) = {5, 6, 7, 8};                 Plane Surface(2) = {2};   // y=YL
Curve Loop(3) = {1, 10, -5, -9};              Plane Surface(3) = {3};   // bottom minus
Curve Loop(4) = {3, 12, -7, -11};             Plane Surface(4) = {4};   // top minus
Curve Loop(5) = {4, 9, -8, -12};              Plane Surface(5) = {5};   // x=XL minus
Curve Loop(6) = {2, 11, -6, -10};             Plane Surface(6) = {6};   // x=XR minus

Surface Loop(1) = {1, 2, 3, 4, 5, 6};
Volume(1) = {1};

// PLUS volume edges
Line(13) = {9, 10};
Line(14) = {10, 11};
Line(15) = {11, 12};
Line(16) = {12, 9};
Line(17) = {1, 9};
Line(18) = {2, 10};
Line(19) = {3, 11};
Line(20) = {4, 12};

Curve Loop(7)  = {13, 14, 15, 16};            Plane Surface(7)  = {7};  // y=YR
Curve Loop(8)  = {1, 18, -13, -17};           Plane Surface(8)  = {8};  // bottom plus
Curve Loop(9)  = {3, 20, -15, -19};           Plane Surface(9)  = {9};  // top plus
Curve Loop(10) = {-4, 20, 16, -17};           Plane Surface(10) = {10}; // x=XL plus
Curve Loop(11) = {2, 19, -14, -18};           Plane Surface(11) = {11}; // x=XR plus

Surface Loop(2) = {1, 7, 8, 9, 10, 11};
Volume(2) = {2};

Field[1] = Distance;
Field[1].FacesList = {1};
Field[2] = MathEval;
Field[2].F = Sprintf("0.05*F1 + (F1/2.5e3)^2 + %g", lc_fault);
Background Field = 2;

Physical Surface(101) = {4, 9};                       // free surface
Physical Surface(103) = {1};                          // dynamic rupture
Physical Surface(105) = {2, 3, 5, 6, 7, 8, 10, 11};   // absorbing

Physical Volume(1) = {1};   // minus side
Physical Volume(2) = {2};   // plus  side

Mesh.MshFileVersion = 2.2;
