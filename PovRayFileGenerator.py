#!/usr/bin/python3

class PovRayFileGenerator(object):
    boilerplate = \
"""
#include "colors.inc"
#include "glass.inc"
#include "textures.inc"
camera {
  location <10, 10, 5>
  look_at <0, 0, 0>
  angle 20 
}
light_source { <-10,50,10> 1 }
background { rgb <0.0, 0.0, 0.0> }
global_settings { ambient_light rgb<1, 1, 1> }
%s
"""

    sphere = \
"""
sphere {
  <%s>, %1.6f texture { pigment { color Yellow }}}
"""

    outer_sphere = \
"""
sphere {
  <%s>, %1.6f texture { NBbeerbottle }}
"""

    cylinder = \
"""
cylinder { %s, %1.6f texture { pigment { color Cyan }}}
"""

    triangle = \
"""
triangle{ %s texture { NBwinebottle } }
"""
    
    def __init__(self):
        pass

    def generate(self, icos, r):
        vertices = icos.vertices
        edges    = icos.edges
        faces    = icos.faces
        sph_R    = icos.sphere_r
        output_str = "" + PovRayFileGenerator.boilerplate
        main_part = ""
        #main_part += (PovRayFileGenerator.outer_sphere % ("0, 0, 0", sph_R))
        for v in vertices:
            main_part += (PovRayFileGenerator.sphere % (str(v), r))
        for edge in edges:
            main_part += (PovRayFileGenerator.cylinder % (edge, r/2.0))
        #for face in faces:
        #    main_part += (PovRayFileGenerator.triangle % str(face))
        return(output_str % main_part)
