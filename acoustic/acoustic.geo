/*
 * Fixed Split Cube for SeisSol
 * Top is Free Surface (101), others are Absorbing (105)
 * Explicitly forcing MSH 2.2 for PUMGen compatibility
 */

size = 1.0;
cl = 0.2; // Mesh spacing

// --- Points ---
Point(1) = {-size, -size, -size, cl}; 
Point(2) = { size, -size, -size, cl}; 
Point(3) = { size,  size, -size, cl}; 
Point(4) = {-size,  size, -size, cl}; 
Point(5) = {-size, -size,  size, cl}; 
Point(6) = { size, -size,  size, cl}; 
Point(7) = { size,  size,  size, cl}; 
Point(8) = {-size,  size,  size, cl}; 

// Interface Points (x = 0)
Point(9)  = {0, -size, -size, cl}; 
Point(10) = {0,  size, -size, cl}; 
Point(11) = {0, -size,  size, cl}; 
Point(12) = {0,  size,  size, cl}; 

// --- Lines ---
Line(1) = {1, 9}; Line(2) = {9, 10}; Line(3) = {10, 4}; Line(4) = {4, 1};
Line(5) = {5, 11}; Line(6) = {11, 12}; Line(7) = {12, 8}; Line(8) = {8, 5}; 
Line(9) = {1, 5}; Line(10) = {9, 11}; Line(11) = {10, 12}; Line(12) = {4, 8}; 
Line(13) = {9, 2}; Line(14) = {2, 3}; Line(15) = {3, 10}; 
Line(16) = {11, 6}; Line(17) = {6, 7}; Line(18) = {7, 12}; 
Line(19) = {2, 6}; Line(20) = {3, 7}; 

// --- Surfaces ---
// Left Volume
Line Loop(1) = {1, 2, 3, 4};       Plane Surface(1) = {1};   // Bottom Left
Line Loop(2) = {5, 6, 7, 8};       Plane Surface(2) = {2};   // Top Left
Line Loop(3) = {1, 10, -5, -9};    Plane Surface(3) = {3};   // Front Left
Line Loop(4) = {2, 11, -6, -10};   Plane Surface(4) = {4};   // INTERFACE (x=0)
Line Loop(5) = {3, 12, -7, -11};   Plane Surface(5) = {5};   // Back Left
Line Loop(6) = {4, 9, -8, -12};    Plane Surface(6) = {6};   // Outer Left (x=-1)

// Right Volume
Line Loop(7) = {13, 14, 15, -2};   Plane Surface(7) = {7};   // Bottom Right
Line Loop(8) = {16, 17, 18, -6};   Plane Surface(8) = {8};   // Top Right
Line Loop(9) = {13, 19, -16, -10}; Plane Surface(9) = {9};   // Front Right
Line Loop(10) = {14, 20, -17, -19}; Plane Surface(10) = {10}; // Outer Right (x=1)
Line Loop(11) = {15, 11, -18, -20}; Plane Surface(11) = {11}; // Back Right (FIXED LOOP)

// --- Volumes ---
Surface Loop(1) = {1, 2, 3, 4, 5, 6};  Volume(1) = {1};
Surface Loop(2) = {7, 8, 9, 10, 11, 4}; Volume(2) = {2};

// --- SeisSol Physical Groups ---
Physical Surface(101) = {2, 8};                      // Top Faces (Free Surface)
Physical Surface(105) = {1, 3, 5, 6, 7, 9, 10, 11}; // External Faces (Absorbing)
Physical Volume(1) = {1};                             // Material x < 0
Physical Volume(2) = {2};                             // Material x > 0

// Force MSH 2.2 format for PUMGen compatibility
Mesh.MshFileVersion = 2.2;
