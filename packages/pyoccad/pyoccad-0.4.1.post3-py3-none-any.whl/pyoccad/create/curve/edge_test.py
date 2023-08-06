from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Shape
from OCC.Core.gp import gp_Elips, gp_Circ, gp_Ax2, gp_Pnt, gp_Dir

from pyoccad.create import CreateCircle, CreateEdge, CreateCurve
from pyoccad.tests.testcase import TestCase


class CreateEdgeTest(TestCase):

    def test_as_edge(self):
        c3d = CreateCircle.from_radius_and_center(1.)
        edge = CreateEdge.from_contour(c3d)
        shape = TopoDS_Shape(edge)

        self.assertIsInstance(shape, TopoDS_Shape)
        self.assertIsInstance(CreateEdge.as_edge(shape), TopoDS_Edge)

    def test_from_contour(self):
        c3d = CreateCircle.from_radius_and_center(1.)
        edge = CreateEdge.from_contour(c3d)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        c3d = gp_Circ(gp_Ax2(gp_Pnt(), gp_Dir(0., 0., 1.)), 5.)
        edge = CreateEdge.from_contour(c3d)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        e3d = gp_Elips(gp_Ax2(gp_Pnt(), gp_Dir(0., 0., 1.)), 10., 5.)
        edge = CreateEdge.from_contour(e3d)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        edge = CreateEdge.from_contour(edge)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        with self.assertRaises(TypeError):
            CreateEdge.from_contour(gp_Pnt())

    def test_from_2_points(self):
        edge = CreateEdge.from_2_points((0., 0., 0.), (1., 1., 1.))
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertFalse(adaptor.IsClosed())

    def test_from_curve(self):
        c3d = CreateCircle.from_radius_and_center(1.)
        edge = CreateEdge.from_curve(c3d)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        c2d = CreateCircle.from_3d(c3d)
        edge = CreateEdge.from_curve(c2d)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        with self.assertRaises(TypeError):
            CreateEdge.from_curve(gp_Pnt())

    def test_from_adaptor(self):
        c3d = CreateCircle.from_radius_and_center(1.)
        construction_edge = CreateEdge.from_curve(c3d)
        construction_adaptor = BRepAdaptor_Curve(construction_edge)
        edge = CreateEdge.from_adaptor(construction_adaptor)
        self.assertIsInstance(edge, TopoDS_Edge)
        self.assertFalse(edge.IsNull())
        self.assertFalse(edge.Infinite())
        adaptor = BRepAdaptor_Curve(edge)
        self.assertTrue(adaptor.IsClosed())

        # TODO: should be handled as a valid adaptor
        with self.assertRaises(TypeError):
            CreateEdge.from_adaptor(CreateCurve.as_adaptor(c3d))
