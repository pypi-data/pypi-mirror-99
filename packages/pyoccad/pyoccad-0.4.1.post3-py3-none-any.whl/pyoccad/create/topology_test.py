from OCC.Core.Geom import Geom_Plane
from OCC.Core.TopoDS import (TopoDS_Vertex, TopoDS_Edge, TopoDS_Wire, TopoDS_Face,
                             TopoDS_Shell, TopoDS_Solid, TopoDS_Compound)

from pyoccad.create import CreateTopology, CreatePoint, CreateCircle, CreatePlane
from pyoccad.tests.testcase import TestCase


class CreateTopologyTest(TestCase):

    def test_make_vertex(self):
        vertex = CreateTopology.make_vertex(CreatePoint.as_point((10., 20., 30.)))
        self.assertIsInstance(vertex, TopoDS_Vertex)

    def test_make_edge(self):
        edge = CreateTopology.make_edge(CreateCircle.from_radius_and_center(1, (10, 10, 10)))
        self.assertIsInstance(edge, TopoDS_Edge)

    def test_make_wire(self):
        edge = CreateTopology.make_edge(CreateCircle.from_radius_and_center(1, (10, 10, 10)))
        wire = CreateTopology.make_wire(edge)
        self.assertIsInstance(wire, TopoDS_Wire)

    def test_make_face(self):
        face = CreateTopology.make_face(CreatePlane.xoy())
        self.assertIsInstance(face, TopoDS_Face)

    def test_make_shell(self):
        shell = CreateTopology.make_shell(Geom_Plane(CreatePlane.xoy()))
        self.assertIsInstance(shell, TopoDS_Shell)

    def test_make_solid(self):
        shell = CreateTopology.make_shell(Geom_Plane(CreatePlane.xoy()))
        solid = CreateTopology.make_solid(shell)
        self.assertIsInstance(solid, TopoDS_Solid)

    def test_make_compound(self):
        shell = CreateTopology.make_shell(Geom_Plane(CreatePlane.xoy()))
        solid = CreateTopology.make_solid(shell)
        compound = CreateTopology.make_compound(solid)
        self.assertIsInstance(compound, TopoDS_Compound)
