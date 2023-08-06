from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Shape, TopoDS_Vertex
from OCC.Core.gp import gp_Elips, gp_Circ, gp_Ax2, gp_Pnt, gp_Dir

from pyoccad.create import CreateCircle, CreateEdge, CreateCurve, CreateVertex, CreatePoint
from pyoccad.tests.testcase import TestCase


class CreatVertexTest(TestCase):

    def test_from_point(self):
        vertex = CreateVertex.from_point((10., 20., 30.))
        self.assertIsInstance(vertex, TopoDS_Vertex)

        point = CreatePoint.from_vertex(vertex)
        self.assertIsInstance(point, gp_Pnt)
        self.assertAlmostSameCoord(point, (10., 20., 30.))

