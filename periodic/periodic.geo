SetFactory("OpenCASCADE");
side_length=1;
average_mesh_element_size=0.1;
mesh_element_size_perturbation=0.03;

Box(1) = {-side_length,-side_length,-side_length,2*side_length,2*side_length,2*side_length};

//Periodic BC
Periodic Surface {2} = {1} Translate {side_length*2, 0, 0};
Periodic Surface {4} = {3} Translate {0, side_length*2, 0};
Periodic Surface {6} = {5} Translate {0, 0, side_length*2};

//Fields for slight variation across the cube
Field[1] = MathEval;
Field[1].F = average_mesh_element_size + mesh_element_size_perturbation*(
    "0.4*sin(5*x)*cos(7*y)*sin(3*z) 
  + 0.3*sign(sin(13*x)*cos(17*y)) 
  + 0.3*(2*floor(5*z)/5 - 1)"
);

Background Field = 1;




// Mesh settings
Mesh.ElementOrder = 1;   // linear tetrahedra
Mesh.Algorithm3D = 4;    // Delaunay
Mesh 3;                  // generate 3D mesh

