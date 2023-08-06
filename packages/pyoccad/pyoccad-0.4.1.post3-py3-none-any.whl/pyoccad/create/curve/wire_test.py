from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.TopoDS import TopoDS_Wire
from OCC.Core.gp import gp_Circ, gp_Ax2, gp_Pnt, gp_Dir

from pyoccad.create import CreateBezier, CreateCircle, CreateCurve, CreateWire, CreatePlane, CreatePoint
from pyoccad.explore import ExploreSubshapes
from pyoccad.measure import MeasureCurve
from pyoccad.tests.testcase import TestCase


class TestWire(TestCase):

    def test_from_elements(self):
        c1 = CreateBezier.from_poles([[0, 0], [1, 0]])
        c2 = CreateBezier.from_poles([[1, 0, 0], [1, 1, 0]])
        e1 = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([1, 1, 0]),
                                     CreatePoint.as_point([1, 1, 1])).Edge()
        e2 = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([1, 1, 1]),
                                     CreatePoint.as_point([1, 1, 2])).Edge()
        e3 = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([1, 1, 2]),
                                     CreatePoint.as_point([3, 1, 2])).Edge()
        w1 = BRepBuilderAPI_MakeWire(e2, e3).Wire()

        w2 = CreateWire.from_elements([c1, c2, e1, w1])
        self.assertTrue(isinstance(w2, TopoDS_Wire))

        with self.assertRaises(TypeError):
            CreateWire.from_element((True,))

    def test_from_element(self):
        c1 = CreateBezier.from_poles([[0, 0], [1, 0]])
        c2 = CreateBezier.from_poles([[1, 0, 0], [1, 1, 0]])
        c3 = CreateCircle.from_3_points(([1, 0, 0], [1, 1, 0], [2, 2, 0]))
        c4 = gp_Circ(gp_Ax2(gp_Pnt(), gp_Dir(0., 0., 1.)), 5.)
        a1 = CreateCurve.as_adaptor(c3)
        e1 = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([1, 1, 0]),
                                     CreatePoint.as_point([1, 1, 1])).Edge()
        e2 = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([1, 1, 1]),
                                     CreatePoint.as_point([1, 1, 2])).Edge()
        e3 = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([1, 1, 2]),
                                     CreatePoint.as_point([3, 1, 2])).Edge()
        elements = [c1, c2, c3, c4, e1, e2, e3, a1]
        for element in elements:
            w = CreateWire.from_element(element)
            self.assertTrue(isinstance(w, TopoDS_Wire))

        w = CreateWire.from_element(w)
        self.assertTrue(isinstance(w, TopoDS_Wire))

        with self.assertRaises(TypeError):
            CreateWire.from_element(True)

    def test_from_plane_and_sizes(self):
        w = CreateWire.from_plane_and_sizes(CreatePlane.xoy(), 1, 1)
        self.assertAlmostEqualValues(MeasureCurve.length(w), 4.)

    def test_from_points(self):
        points = [(0., 0., 0), (1., 1., 1.), (2., 2., 20.)]
        w = CreateWire.from_points(points)
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertFalse(w.Closed())
        for i, v in enumerate(ExploreSubshapes.get_vertices(w)):
            self.assertEqual(CreatePoint.from_vertex(v).Coord(), points[i])

        w = CreateWire.from_points(points, auto_close=True)
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertTrue(w.Closed())
