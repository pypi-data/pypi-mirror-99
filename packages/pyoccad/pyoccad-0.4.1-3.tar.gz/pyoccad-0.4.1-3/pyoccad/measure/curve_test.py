from math import pi

from OCC.Core.Geom import Geom_Curve
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_HCurve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pnt2d, gp_Dir2d

from pyoccad.create import CreateCircle, CreateEdge, CreateWire
from pyoccad.measure.curve import MeasureCurve
from pyoccad.tests.testcase import TestCase, tol, angTol


class MeasureCurveTest(TestCase):

    def test_length(self):
        r = 1.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertAlmostEqual(MeasureCurve.length(c), pi * 2 * r, delta=tol)

        r = 2.
        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertAlmostEqual(MeasureCurve.length(c2d), pi * 2 * r, delta=tol)

        r = 3.
        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(e, TopoDS_Edge)
        self.assertAlmostEqual(MeasureCurve.length(e), pi * 2 * r, delta=tol)

        r = 4.
        w = CreateWire.from_element(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertAlmostEqual(MeasureCurve.length(w), pi * 2 * r, delta=tol)

        r = 5.
        a = GeomAdaptor_Curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(a, GeomAdaptor_Curve)
        self.assertAlmostEqual(MeasureCurve.length(a), pi * 2 * r, delta=tol)

        r = 6.
        a2d = Geom2dAdaptor_Curve(CreateCircle.from_3d(CreateCircle.from_radius_and_center(r)))
        self.assertIsInstance(a2d, Geom2dAdaptor_Curve)
        self.assertAlmostEqual(MeasureCurve.length(a2d), pi * 2 * r, delta=tol)

    def test_value(self):
        r = 1.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertAlmostSameCoord(MeasureCurve.value(c, 0.), (1., 0., 0.))

    def test_derivatives(self):
        r = 1.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertAlmostSameCoord(MeasureCurve.derivatives(c, 0., 0), (1., 0., 0.))
        self.assertAlmostSameCoord(MeasureCurve.derivatives(c, 0., 1)[1], (0., 1., 0.))
        self.assertAlmostSameCoord(MeasureCurve.derivatives(c, 0., 2)[2], (-1., 0., 0.))
        self.assertAlmostSameCoord(MeasureCurve.derivatives(c, 0., 3)[3], (0., -1., 0.))
        self.assertAlmostSameCoord(MeasureCurve.derivatives(c, 0., 4)[4], (1., 0., 0.))

    def test_fraction_length(self):
        r = 1.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertAlmostEqual(MeasureCurve.fraction_length(c, pi, 2 * pi), pi * r, delta=tol)

        r = 2.
        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertAlmostEqual(MeasureCurve.fraction_length(c2d, pi, 2 * pi), pi * r, delta=tol)

        r = 3.
        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(e, TopoDS_Edge)
        self.assertAlmostEqual(MeasureCurve.fraction_length(e, pi, 2 * pi), pi * r, delta=tol)

        r = 4.
        w = CreateWire.from_element(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertAlmostEqual(MeasureCurve.fraction_length(w, 0.5, 1), pi * r, delta=tol)

        r = 5.
        a = GeomAdaptor_Curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(a, GeomAdaptor_Curve)
        self.assertAlmostEqual(MeasureCurve.fraction_length(a, pi, 2 * pi), pi * r, delta=tol)

        r = 6.
        a = Geom2dAdaptor_Curve(CreateCircle.from_3d(CreateCircle.from_radius_and_center(r)))
        self.assertIsInstance(a, Geom2dAdaptor_Curve)
        self.assertAlmostEqual(MeasureCurve.fraction_length(a, pi, 2 * pi), pi * r, delta=tol)

    def test_relative_curvilinear_abs(self):
        r = 2.
        c = CreateCircle.from_radius_and_center(r)
        self.assertAlmostEqual(MeasureCurve.position_from_relative_curvilinear_abs_with_start(c, 0.5, pi / 2),
                               pi + pi / 2, delta=tol)
        self.assertAlmostEqual(MeasureCurve.position_from_relative_curvilinear_abs(c, 0.5), pi, delta=tol)

    def test_center_of_curvature(self):
        r = 2.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        pc = MeasureCurve.center_of_curvature(c, 0.5)
        d = pc.Distance(gp_Pnt())
        self.assertIsInstance(pc, gp_Pnt)
        self.assertAlmostEqual(d, 0., delta=tol)

        e = CreateEdge.from_curve(c)
        brep_adaptor = BRepAdaptor_Curve(e)
        pc = MeasureCurve.center_of_curvature(brep_adaptor, 0.5)
        d = pc.Distance(gp_Pnt())
        self.assertIsInstance(pc, gp_Pnt)
        self.assertAlmostEqual(d, 0., delta=tol)

        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        pc = MeasureCurve.center_of_curvature(c2d, 0.5)
        self.assertIsInstance(pc, gp_Pnt2d)
        d = pc.Distance(gp_Pnt2d())
        self.assertAlmostEqual(d, 0., delta=tol)

        with self.assertRaises(TypeError):
            MeasureCurve.center_of_curvature('null', 0)
        with self.assertRaises(TypeError):
            MeasureCurve.center_of_curvature(10, 0)
        with self.assertRaises(TypeError):
            MeasureCurve.center_of_curvature((0., 2), 0)

    def test_curvature(self):
        r = 2.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertAlmostEqual(MeasureCurve.curvature(c, 0.5), 1. / r, delta=tol)

        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertAlmostEqual(MeasureCurve.curvature(c2d, 0.5), 1. / r, delta=tol)

        with self.assertRaises(TypeError):
            MeasureCurve.curvature('null', 0)
        with self.assertRaises(TypeError):
            MeasureCurve.curvature(10, 0)
        with self.assertRaises(TypeError):
            MeasureCurve.curvature((0., 2), 0)

    def test_tangent(self):
        r = 2.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertTrue(MeasureCurve.tangent(c, 0).IsEqual(gp_Dir(0, 1, 0), angTol))

        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertTrue(MeasureCurve.tangent(c2d, 0).IsEqual(gp_Dir2d(0, 1), angTol))

        with self.assertRaises(TypeError):
            MeasureCurve.tangent('null', 0)
        with self.assertRaises(TypeError):
            MeasureCurve.tangent(10, 0)
        with self.assertRaises(TypeError):
            MeasureCurve.tangent((0., 2), 0)

    def test_normal(self):
        r = 2.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertTrue(MeasureCurve.normal(c, 0).IsEqual(gp_Dir(-1, 0, 0), angTol))

        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertTrue(MeasureCurve.normal(c2d, 0).IsEqual(gp_Dir2d(-1, 0), angTol))

        with self.assertRaises(TypeError):
            MeasureCurve.normal('null', 0)
        with self.assertRaises(TypeError):
            MeasureCurve.normal(10, 0)
        with self.assertRaises(TypeError):
            MeasureCurve.normal((0., 2), 0)
