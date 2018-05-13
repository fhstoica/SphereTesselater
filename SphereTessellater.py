#!/usr/bin/python3

import numpy as np
from PovRayFileGenerator import PovRayFileGenerator

class Vertex(object):
    def __init__(self, coords, Id):
        self.x            = coords[0]
        self.y            = coords[1]
        self.z            = coords[2]
        self.eps          = 1.0e-6
        self.digits       = 6
        self.Id           = Id
        self.coords_tuple = (round(self.x, self.digits), 
                             round(self.y, self.digits), 
                             round(self.z, self.digits))

    def __eq__(self, other):
        return(self.Id == other.Id)

    def __str__(self):
        return("%1.3f, %1.3f, %1.3f" % (self.x, self.y, self.z))

    def __hash__(self):
        return(self.Id)

    @staticmethod
    def dist(v1, v2):
        return(np.sqrt(np.power(v1.x - v2.x, 2) + 
                       np.power(v1.y - v2.y, 2) + 
                       np.power(v1.z - v2.z, 2)))

class Edge(object):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.coords_tuple = tuple(list(v1.coords_tuple) + list(v2.coords_tuple))

    def __eq__(self, other):
        return((self.v1 == other.v1 and self.v2 == other.v2) or 
               (self.v1 == other.v2 and self.v2 == other.v1))

    def __str__(self):
        return("<%s>, <%s>" % (self.v1, self.v2))
        
    def __hash__(self):
        return((self.v1.Id, self.v2.Id).__hash__() ^ 
               (self.v2.Id, self.v1.Id).__hash__())

class Face(object):
    def __init__(self, e1, e2, e3):
        self.e1           = e1
        self.e2           = e2
        self.e3           = e3
        self.v_list       = list(self.getVertices(e1, e2, e3))
        self.coords_tuple = self.createCoordsTuple(self.v_list)

    def getVertices(self, e1, e2, e3):
        v_set = set()
        v_set.add(e1.v1)
        v_set.add(e1.v2)
        v_set.add(e2.v1)
        v_set.add(e2.v2)
        v_set.add(e3.v1)
        v_set.add(e3.v2)
        return(v_set)
    
    def createCoordsTuple(self, vertex_list):
        x_c = round((vertex_list[0].coords_tuple[0] + 
                     vertex_list[1].coords_tuple[0] + 
                     vertex_list[2].coords_tuple[0])/3, 6)
        y_c = round((vertex_list[0].coords_tuple[1] + 
                     vertex_list[1].coords_tuple[1] + 
                     vertex_list[2].coords_tuple[1])/3, 6)
        z_c = round((vertex_list[0].coords_tuple[2] + 
                     vertex_list[1].coords_tuple[2] + 
                     vertex_list[2].coords_tuple[2])/3, 6)
        S = (x_c, y_c, z_c)
        return(S)

    def __eq__(self, other):
        this_id_set = set([v.Id for v in self.v_list])
        other_id_set = set([v.Id for v in other.v_list])
        return(len(this_id_set & other_id_set) == 3)

    def __str__(self):
        return("<%s>, <%s>, <%s>" % (self.v_list[0], self.v_list[1], self.v_list[2]))

    def __hash__(self):
        return(self.e1.__hash__() ^ self.e2.__hash__() ^ self.e3.__hash__())

class IcosahedronGenerator(object):
    def __init__(self):
        self.eps      = 1.0e-6

    def generate(self):
        golden_r = (1.0 + np.sqrt(5.0))/2.0
        primary_vertices = []
        for i in range(2):
            for j in range(2):
                primary_vertices.append((0, np.power(-1, i), golden_r*np.power(-1, j)))
                
        all_vertices = []
        for k in range(3):
            for v in primary_vertices:
                all_vertices.append((v[((k+0)%3)], v[((k+1)%3)], v[((k+2)%3)]))

        vertices  = [Vertex(all_vertices[i], i) for i in range(len(all_vertices))]
        return(vertices)

    def generateEdges(self, vertices):
        starting_vertex      = vertices[0]
        unprocessed_vertices = vertices[1:]
        edges                = []
        dist_list            = list(set([Vertex.dist(starting_vertex, v) for v in unprocessed_vertices]))
        dist_list.sort()
        edge_length          = dist_list[0]
        for i in range(len(vertices)):
            for j in range(i+1, len(vertices)):
                edge = Edge(vertices[i], vertices[j])
                if (abs(Vertex.dist(edge.v1, edge.v2) - edge_length) < self.eps) and (edge not in edges):
                    edges.append(edge)
        return(edges)

    def generateFaces(self, vertices, edges):
        faces = []
        for i in range(len(edges)):
            for j in range(i+1, len(edges)):
                if (edges[i].v1==edges[j].v1 or
                    edges[i].v1==edges[j].v2 or
                    edges[i].v2==edges[j].v1 or
                    edges[i].v2==edges[j].v2):
                    
                    v_list   = [edges[i].v1, edges[j].v1, edges[i].v2, edges[j].v2]
                    v_count  = {v:v_list.count(v) for v in v_list}
                    common_v = [key for key,val in v_count.items() if val == 2][0]
                    other_vs = [key for key,val in v_count.items() if val == 1]
                    if (abs(Vertex.dist(common_v, other_vs[0]) - Vertex.dist(common_v, other_vs[1]))    < self.eps and 
                        abs(Vertex.dist(common_v, other_vs[1]) - Vertex.dist(other_vs[1], other_vs[0])) < self.eps and 
                        abs(Vertex.dist(other_vs[1], other_vs[0]) - Vertex.dist(common_v, other_vs[1])) < self.eps):
                        faces.append(Face(edges[i], edges[j], Edge(other_vs[0], other_vs[1])))

        filtered_faces = []
        for face in faces:
            if face not in filtered_faces:
                filtered_faces.append(face)

        return(filtered_faces)

class Icosahedron(object):
    def __init__(self, vertices, edges, faces):
        self.vertices = [v for v in vertices]
        self.edges    = [ed for ed in edges]
        self.faces    = [f for f in faces]
        self.edges_from_vertices = None
        self.faces_from_edges    = None
        self.sphere_r = self.findSphereRadius()
        self.setUp()

    def findSphereRadius(self):
        r = (1.0/2.0)*np.sqrt(10.0 + 2*np.sqrt(5))
        return(r)

    def setUp(self):
        self.edges_from_vertices = {}    
        for edge in self.edges:
            for v in [edge.v1, edge.v2]:
                if v not in self.edges_from_vertices.keys():
                    self.edges_from_vertices[v] = [edge]
                else:
                    self.edges_from_vertices[v].append(edge)
                
        self.faces_from_edges = {}
        for face in self.faces:
            for edge in [face.e1, face.e2, face.e3]:
                if edge not in self.faces_from_edges.keys():
                    self.faces_from_edges[edge] = [face]
                else:
                    self.faces_from_edges[edge].append(face)

class SphereTessellater(object):
    def __init__(self):
        pass
        
    def refineMesh(self, input_mesh):
        vertex_ids = [v.Id for v in input_mesh.vertices]
        vertex_ids.sort()
        last_id                 = vertex_ids[-1]
        edges                   = input_mesh.edges
        counter                 = 1
        edges_with_new_vertices = []
        new_edges_and_old       = []
        new_edges               = {} 
        
        ###############################################
        # Add a new vertex in the middle of each edge #
        # Also split each edge into two edges         #
        ###############################################
        for edge in edges:
            mid_x = (edge.v1.x + edge.v2.x)/2
            mid_y = (edge.v1.y + edge.v2.y)/2
            mid_z = (edge.v1.z + edge.v2.z)/2

            r   = np.sqrt(np.power(mid_x, 2) + np.power(mid_y, 2) + np.power(mid_z, 2))
            r_0 = np.sqrt(np.power(edge.v1.x, 2) + np.power(edge.v1.y, 2) + np.power(edge.v1.z, 2))
            scaler = r_0/r
            
            mid_x *= scaler
            mid_y *= scaler
            mid_z *= scaler

            new_vertex = Vertex((mid_x, mid_y, mid_z), last_id + counter)
            edges_with_new_vertices.append((edge, new_vertex))
            
            new_edges_and_old.append((edge, Edge(edge.v1, new_vertex), Edge(new_vertex, edge.v2)))
            new_edges[edge] = [new_vertex]
            new_edges[edge].append(Edge(edge.v1, new_vertex))
            new_edges[edge].append(Edge(new_vertex, edge.v2))
            
            counter += 1
            
        new_vertices = input_mesh.vertices + [v[1] for v in edges_with_new_vertices]

        #########################################
        # Split each existing face into 4 faces #
        #########################################
        new_faces        = set()
        cross_face_edges = set()
        for edge in new_edges.keys():
            middle_vertex = new_edges[edge][0]
            sub_edges     = new_edges[edge][1:]
            for f in input_mesh.faces_from_edges[edge]:
                for k_edge in [f.e1, f.e2, f.e3]:
                    if k_edge != edge:
                        middle_f_vertex = new_edges[k_edge][0]
                        cross_face_edges.add(Edge(middle_vertex, middle_f_vertex))

                m_v1   = new_edges[f.e1][0] 
                m_v2   = new_edges[f.e2][0]
                m_v3   = new_edges[f.e3][0]
                center_face = Face(Edge(m_v1, m_v2), Edge(m_v2, m_v3), Edge(m_v3, m_v1))
                new_faces.add(center_face)
            
                edge_pairs = [(f.e1, f.e2), (f.e2, f.e3), (f.e3, f.e1)]
                for edge_pair in edge_pairs:
                    v_list      = [edge_pair[0].v1, edge_pair[1].v1, edge_pair[0].v2, edge_pair[1].v2]
                    v_count     = {v:v_list.count(v) for v in v_list}
                    common_v    = [key for key,val in v_count.items() if val == 2][0]
                    m_vertex_0  = new_edges[edge_pair[0]][0]
                    m_vertex_1  = new_edges[edge_pair[1]][0]
                    corner_face = Face(Edge(common_v, m_vertex_0),
                                       Edge(m_vertex_0, m_vertex_1),
                                       Edge(m_vertex_1, common_v))
                    new_faces.add(corner_face)
          
        #########################################
        # Create a new polyhedreon from the new #
        # vertices, edges and faces             #
        #########################################
        combined_new_vertices = new_vertices
        combined_new_edges    = [ed for ed in cross_face_edges]
        for edge_key in new_edges.keys():
            combined_new_edges.extend(new_edges[edge_key][1:])
        combined_new_faces = list(new_faces)
        output_mesh = Icosahedron(combined_new_vertices, combined_new_edges, combined_new_faces)
        return(output_mesh)

    def tesselate(self, depth):
        pass


def printPolyhedronStats(L):
    print("\n".join(["Vertex : %s %s" % (k.Id, " ".join(["[%s - %s]" % (s.v1.Id, s.v2.Id) for s in ve])) for k,ve in L[-1].edges_from_vertices.items()]))
    print("\n".join(["Edge : %s %s" % ("[%s - %s]" % (edge.v1.Id, edge.v2.Id), ["[%s - %s - %s]" % (f.v_list[0].Id, f.v_list[1].Id, f.v_list[2].Id) for f in f_list]) for edge,f_list in L[-1].faces_from_edges.items()]))
    
    print("\n".join(["V: %s F: %s E: %s" % (len(ic.vertices), len(ic.faces), len(ic.edges)) for ic in L]))

def testPovRayFileGen():
    G = IcosahedronGenerator()
    V = G.generate()
    E = G.generateEdges(V)
    F = G.generateFaces(V, E)
    I = Icosahedron(V, E, F)
    ST = SphereTessellater()
    I2 = ST.refineMesh(I)
    I3 = ST.refineMesh(I2)
    I4 = ST.refineMesh(I3)
    I5 = ST.refineMesh(I4)
    
    ####################################################
    # Uncomment the lines below to see the number of   #
    # vertices, edges and faces generated at each step # 
    ####################################################
    #L = [I, I2, I3, I4, I5]
    #printPolyhedronStats(L)

    P = PovRayFileGenerator()
    s = P.generate(I5, 0.01)
    
    print(s)

def main():
    testPovRayFileGen()

if __name__ == "__main__":
    main()
