import numpy as np
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Vertex, TopoDS_Edge
from OCC.Core.gp import gp_XYZ

from pyoccad.create import (CreatePoint, CreateVertex, CreateBSpline, CreateEdge, CreateBox, CreateWire,
                            CreateExtrusion, CreateVector, CreateTopology)
from pyoccad.explore.subshapes import ExploreSubshapes
from pyoccad.tests.testcase import TestCase, tol


class ExploreSubshapesTest(TestCase):

    def test_cast_type(self):
        vertex = CreateVertex.from_point((1., 2., 3.))
        shape = TopoDS_Shape(vertex)
        casted_shape = ExploreSubshapes.cast_shape(shape, TopAbs_VERTEX)
        self.assertIsInstance(casted_shape, TopoDS_Vertex)

        point = CreatePoint.from_vertex(casted_shape)
        self.assertAlmostSameCoord(point, (1., 2., 3.))

        casted_shape = ExploreSubshapes.cast_shape(shape, 'vertex')
        self.assertIsInstance(casted_shape, TopoDS_Vertex)

        with self.assertRaises(TypeError):
            ExploreSubshapes.cast_shape(shape, np.r_[1.])

        with self.assertRaises(TypeError):
            ExploreSubshapes.cast_shape(shape, 18)

    def test_get_subshapes(self):
        box = BRepPrimAPI_MakeBox(1, 2, 3).Solid()
        vertices = [*ExploreSubshapes.get_subshapes(box, 'vertex')]
        self.assertEqual(8, len(vertices))

    def test_get_vertices(self):
        box = BRepPrimAPI_MakeBox(1, 2, 3).Solid()
        vertices = [*ExploreSubshapes.get_vertices(box)]
        self.assertEqual(8, len(vertices))

        points = [CreatePoint.from_vertex(v) for v in vertices]
        expected_points = [(0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (0.0, 2.0, 3.0), (0.0, 2.0, 0.0),
                           (1.0, 0.0, 3.0), (1.0, 0.0, 0.0), (1.0, 2.0, 3.0), (1.0, 2.0, 0.0)]

        for box_point in expected_points:
            self.assertTrue(any([(pt.XYZ() - gp_XYZ(*box_point)).Modulus() <= tol for pt in points]))

    def test_get_shapes(self):

        spline1 = CreateBSpline.from_points(((0., 0., 0.), (1., 1., 0.)))
        spline2 = CreateBSpline.from_points(((1., 1., 0.), (2., 2., 0.)))
        edge1 = CreateEdge.from_curve(spline1)
        edge2 = CreateEdge.from_curve(spline2)
        wire = CreateWire.from_elements((edge1, edge2))

        surface = CreateExtrusion.curve(wire, CreateVector.as_vector((0., 0., 10.)))

        shells = [*ExploreSubshapes.get_shells(surface)]
        self.assertEqual(1, len(shells))

        faces = [*ExploreSubshapes.get_faces(surface)]
        self.assertEqual(2, len(faces))

        wires = [*ExploreSubshapes.get_wires(surface)]
        self.assertEqual(2, len(wires))

        edges = [*ExploreSubshapes.get_edges(surface)]
        self.assertEqual(7, len(edges))

        vertices = [*ExploreSubshapes.get_vertices(surface)]
        self.assertEqual(6, len(vertices))

        solid1 = CreateExtrusion.surface(faces[0], CreateVector.as_vector((1., 0., 0.)))
        solid2 = CreateExtrusion.surface(faces[1], CreateVector.as_vector((1., 0., 0.)))
        compound = CreateTopology.make_compound(solid1, solid2)
        compsolid = CreateTopology.make_compsolid(solid1, solid2)

        solids = [*ExploreSubshapes.get_solids(solid1)]
        self.assertEqual(1, len(solids))

        compounds = [*ExploreSubshapes.get_compounds(compound)]
        self.assertEqual(1, len(compounds))

        compsolids = [*ExploreSubshapes.get_compsolids(compsolid)]
        self.assertEqual(1, len(compsolids))

    def test_touching_edges(self):
        box1 = CreateBox.from_dimensions_and_center((1, 1, 1))
        box2 = CreateBox.from_dimensions_and_center((1, 1, 1), (1., 0., 0.))

        box1_shape = TopoDS_Shape(box1)
        box2_shape = TopoDS_Shape(box2)

        edges = ExploreSubshapes.edges_touching_shape(box1_shape, [box2_shape])
        self.assertEqual(4, len(edges))

        points = set([CreatePoint.from_vertex(v).Coord()
                      for v in ExploreSubshapes.get_vertices(CreateWire.from_elements(edges))])
        self.assertEqual({(0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5)},
                         points)
