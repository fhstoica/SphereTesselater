# SphereTessellater
How to tessellate a sphere with triangles

This project consists of two python scripts that will generate a tessellation of the sphere starting from the inscribed icosahedron. The end results is a pov-ray file that can be used to generate an image of the resulting mesh. 

We start out with the initial icosahedron and we assign Ids to the vertices which are simply integers from 0 to 11. The Id of each vertex is also used in identifying the edges and the faces of the icosahedron. 

We then refine this initial mesh by adding a vertex in the middle of each edge. The coordinates of the added vertices are then rescaled to place the new vertices on the same sphere as the original vertices. The original edges are replaced by the new edges, and new ones are added to connect the middle points of the edges of each face. 

This is done by the refineMesh() method of the SphereTessellater class. The input is the original mesh, the output is the final, refined, mesh. Therefore, to refine the mesh to the desired granularity the function will have to be called on the result of the previous refinement operation: 

    I = Icosahedron(V, E, F)
    ST = SphereTessellater()
    I2 = ST.refineMesh(I)
    I3 = ST.refineMesh(I2)
    .
    .
    .
    
Please keep in mind that the number of vertices, edges and faces grows exponentially with the number of refinements:
     1  Vertices: 12    Faces: 20    Edges: 30
     2  Vertices: 42    Faces: 80    Edges: 120
     3  Vertices: 162   Faces: 320   Edges: 480
     4  Vertices: 642   Faces: 1280  Edges: 1920
     5  Vertices: 2562  Faces: 5120  Edges: 7680
     6  Vertices: 10242 Faces: 20480 Edges: 30720
     7  Vertices: 40962 Faces: 81920 Edges: 122880

The class "Icosahedron" will contain in addition to the list of vertices, edges and faces, two dictionaries, which I found very useful for my projects:

edges_from_vertices: The keys are the vertices of the mesh and for each key the value is the list of vertices that are connected to the key vertex by an edge. The original icosahedron vertices are connected to 5 other vertices, while the new inserted vertices are connected to 6 other vertices.  

faces_from_edges : The keys are the edges of the mesh and for each edge the value is the list of faces that are bordered by that edge (2 faces for each edge)

To see the content of these two dictionaries use the function printPolyhedronStats().
