from math import pi, sin
from unittest import skip

from OCC.Core.Adaptor2d import Adaptor2d_Curve2d
from OCC.Core.Geom import Geom_Circle
from OCC.Core.Geom2d import Geom2d_Circle, Geom2d_CartesianPoint
from OCC.Core.Geom2d import Geom2d_Line
from OCC.Core.gp import gp_Ax2, gp_Circ, gp_Ax22d, gp_Circ2d, gp_Pnt, gp_Vec, gp_Dir, gp_Pnt2d, gp_Dir2d

from pyoccad.create import (CreateBezier, CreateBSpline, CreateCircle, CreateCurve, CreateIntersection,
                            CreatePoint, CreateCoordSystem)
from pyoccad.tests.testcase import TestCase, tol, angTol


class CreateCircleTest(TestCase):

    def test___get_extrema(self):
        c1 = CreateCircle.from_radius_and_center(10, gp_Pnt())
        c2 = CreateCircle.from_radius_and_center(100, gp_Pnt())

        self.assertEqual(10, CreateCircle._CreateCircle__get_extrema((c1, c2), use_smallest=True).Radius())
        self.assertEqual(100, CreateCircle._CreateCircle__get_extrema((c1, c2), use_smallest=False).Radius())

        with self.assertRaises(ArithmeticError):
            CreateCircle._CreateCircle__get_extrema([], True)

    def test_from_3_points(self):
        p1 = (1, 0, 0)
        p2 = (0, 1, 0)
        p3 = gp_Pnt(-1, 0, 0)
        c = CreateCircle.from_3_points((p1, p2, p3))
        self.assertAlmostEqual(c.Radius(), 1., delta=tol)
        self.assertAlmostEqual(c.Location().Distance(gp_Pnt()), 0., delta=tol)
        self.assertTrue(c.Axis().Direction().IsEqual(gp_Dir(0, 0, 1), angTol))
        self.assertAlmostEqual(c.Circ().Distance(
            CreatePoint.as_point(p1)), 0., delta=tol)
        self.assertAlmostEqual(c.Circ().Distance(
            CreatePoint.as_point(p2)), 0., delta=tol)
        self.assertAlmostEqual(c.Circ().Distance(
            CreatePoint.as_point(p3)), 0., delta=tol)

        with self.assertRaises(AttributeError):
            CreateCircle.from_3_points((p1, p2, p3, gp_Pnt()))
        with self.assertRaises(AttributeError):
            CreateCircle.from_3_points((p1, p2))

    def test_from_radius_and_center(self):
        c = CreateCircle.from_radius_and_center(2., (1, 2, 3), (0, 0, 1))
        self.assertAlmostEqual(c.Radius(), 2., delta=tol)
        self.assertAlmostEqual(c.Location().Distance(
            gp_Pnt(1, 2, 3)), 0., delta=tol)
        self.assertTrue(c.Axis().Direction().IsEqual(gp_Dir(0, 0, 1), angTol))

    def test_from_radius_and_axis(self):
        ax2 = CreateCoordSystem.from_location_and_directions([0, 0, 0], [1, 0, 0], [0, 0, 1])
        c = CreateCircle.from_radius_and_axis(3, ax2)
        self.assertAlmostEqual(c.Radius(), 3., delta=tol)
        self.assertAlmostEqual(c.Location().Distance(gp_Pnt()), 0., delta=tol)
        self.assertTrue(c.Axis().Direction().IsEqual(gp_Dir(0, 0, 1), angTol))
        self.assertAlmostEqual(c.Location().Translated(
            gp_Vec(ax2.XDirection()) * 3).Distance(c.Value(0)), 0., delta=tol)

    def test_bi_tangent_with_position(self):
        p = gp_Pnt2d(-0.5, 0.)
        d1 = gp_Dir2d(1, 0)
        d2 = d1.Rotated(pi / 3)
        line1 = Geom2d_Line(p, d1)
        line2 = Geom2d_Line(p, d2)
        c = CreateCircle.bi_tangent_with_position(line1, line2, 0.5, tol)
        theoretical_center = gp_Pnt2d(0, sin(pi / 3.) / 3)
        self.assertAlmostSameCoord(c.Location(), theoretical_center)

        c2 = CreateCircle.bi_tangent_with_position(line1, line2, 0.5, tol, 0.5)
        self.assertAlmostSameCoord(c2.Location(), theoretical_center)

        d3 = d1.Rotated(pi / 2)
        line3 = Geom2d_Line(p, d3)
        with self.assertRaises(AttributeError):
            CreateCircle.bi_tangent_with_position(line1, line3, 0., tol)

    def test_tri_tangent(self):
        p1 = gp_Pnt2d(-0.5, 0.)
        p2 = gp_Pnt2d(0.5, 0.)
        d1 = gp_Dir2d(1, 0)
        d2 = d1.Rotated(pi / 3)
        d3 = d2.Rotated(pi / 3)
        l1 = Geom2d_Line(p1, d1)
        l2 = Geom2d_Line(p1, d2)
        l3 = Geom2d_Line(p2, d3)
        c = CreateCircle.tri_tangent((l1, l2, l3), tol)
        theoretical_center = gp_Pnt2d(0, sin(pi / 3.) / 3)
        self.assertAlmostEqual(c.Location().Distance(theoretical_center), 0., delta=tol)

    def test_bi_tangent_with_radius(self):
        b1 = CreateBezier.from_poles([[0, 0], [1, 0]])
        b2 = CreateBezier.from_poles([[0, 0], [0, 1]])
        c = CreateCircle.bi_tangent_with_radius(b1, b2, 1., tol)
        theoretical_center = gp_Pnt2d(1., 1.)
        self.assertAlmostEqual(c.Location().Distance(theoretical_center), 0., delta=tol)

        adaptor1 = CreateCurve.as_adaptor(b1)
        adaptor2 = CreateCurve.as_adaptor(b2)
        self.assertIsInstance(adaptor1, Adaptor2d_Curve2d)
        self.assertIsInstance(adaptor2, Adaptor2d_Curve2d)

        c = CreateCircle.bi_tangent_with_radius(adaptor1, adaptor2, 1., tol)
        theoretical_center = gp_Pnt2d(1., 1.)
        self.assertAlmostEqual(c.Location().Distance(theoretical_center), 0., delta=tol)

    def test_tangent_and_center(self):
        r = 2
        big_circle = gp_Circ2d(gp_Ax22d(gp_Pnt2d(), gp_Dir2d(1, 0), gp_Dir2d(0, 1)), r)
        small_circle = CreateCircle.tangent_and_center(Geom2d_Circle(big_circle), gp_Pnt2d(0., -r / 2), tol)
        self.assertAlmostEqual(small_circle.Radius(), r / 2, delta=tol)

        small_circle = CreateCircle.tangent_and_center(Geom2d_Circle(big_circle),
                                                       Geom2d_CartesianPoint(0., -r / 2),
                                                       tol)
        self.assertAlmostEqual(small_circle.Radius(), r / 2, delta=tol)

        small_circle = CreateCircle.tangent_and_center(Geom2d_Circle(big_circle),
                                                       (0., -r / 2),
                                                       tol)
        self.assertAlmostEqual(small_circle.Radius(), r / 2, delta=tol)

    @skip('skip the rolling ball test, failing for the moment')
    def test_rolling_ball(self):
        bez1 = CreateBezier.from_poles([[0, -0.25], [0.5, -0.25]])
        bez2 = CreateBezier.from_poles([[0, 0.], [0.1, 0.05], [0.25, 0.0], [0.25, -0.5], [0.5, -0.50]])

        np = 50

        fail_count = 0
        p_list1 = []
        for i in range(np):
            u1 = bez1.FirstParameter() + (bez1.LastParameter() - bez1.FirstParameter()) * i / (np - 1)
            c = CreateCircle.bi_tangent_with_position(bez1, bez2, u1, 1e-6)
            if c is not None:
                p_list1.append((u1, c.Circ2d().Position().Location()))
            else:
                fail_count += 1

        self.assertEqual(0, fail_count)

        fail_count = 0
        p_list2 = []

        for i in range(np):
            u2 = bez2.FirstParameter() + (bez2.LastParameter() - bez2.FirstParameter()) * i / (np - 1)
            c = CreateCircle.bi_tangent_with_position(bez2, bez1, u2, 1e-6)
            if c is not None:
                uc, u1, pc, p1 = CreateIntersection.between_2_curves(c, bez1, 1e-6)
                p_list2.append((u1, c.Circ2d().Position().Location()))
            else:
                fail_count += 1

        self.assertEqual(0, fail_count)

        p_list = sorted(p_list1 + p_list2, key=lambda pos_pt: pos_pt[0])
        crv_c_pt = []
        for u_p in p_list:
            crv_c_pt.append(u_p[1])
        _ = CreateBSpline.from_points_with_smoothing(crv_c_pt, (1, 1, 1), 1e-6)

    def test_from_3d(self):
        c = gp_Circ(gp_Ax2(), 2.)
        c2d = CreateCircle.from_3d(c)
        self.assertAlmostEqual(c.Radius(), c2d.Radius(), delta=tol)

        c = Geom_Circle(c)
        c2d = CreateCircle.from_3d(c)
        self.assertAlmostEqual(c.Circ().Radius(), c2d.Circ2d().Radius(), delta=tol)

        with self.assertRaises(TypeError):
            CreateCircle.from_3d(gp_Pnt())

    def test_from_2d(self):
        c2d = gp_Circ2d(gp_Ax22d(), 2.)
        c = CreateCircle.from_2d(c2d)
        self.assertAlmostEqual(c.Radius(), c2d.Radius(), delta=tol)

        c2d = Geom2d_Circle(c2d)
        c = CreateCircle.from_2d(c2d)
        self.assertAlmostEqual(c.Circ().Radius(), c2d.Circ2d().Radius(), delta=tol)

        with self.assertRaises(TypeError):
            CreateCircle.from_2d(gp_Pnt())
