from math import pi, sqrt

from OCC.Core.Geom import Geom_TrimmedCurve
from OCC.Core.Geom2d import Geom2d_TrimmedCurve
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Pnt2d, gp_Vec2d, gp_Dir2d

from pyoccad.create.axis import CreateAxis
from pyoccad.create.curve.line import CreateLine
from pyoccad.create.curve.bezier import CreateBezier
from pyoccad.create.direction import CreateDirection
from pyoccad.create.point import CreatePoint
from pyoccad.tests.testcase import TestCase


class TestLine(TestCase):

    def test_from_axis(self):
        p = CreatePoint.as_point([0, 1, 0.5])
        d = CreateDirection.as_direction([0, 1, 1])
        D = CreateLine.from_axis(CreateAxis.from_location_and_direction(p, d))
        self.assertAlmostSameCoord(D.Value(1), CreatePoint.as_point([0, 1 + 1 / sqrt(2), 0.5 + 1 / sqrt(2)]))

    def test_tangent_to_curve(self):
        poles = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
        ]
        bez = CreateBezier.from_poles(poles)
        u = 0.5
        l = CreateLine.tangent_to_curve(bez, u)
        p1 = gp_Pnt()
        p2 = gp_Pnt()
        t1 = gp_Vec()
        t2 = gp_Vec()
        bez.D1(u, p1, t1)
        l.D1(0, p2, t2)
        self.assertAlmostSameCoord(p1, p2)
        self.assertAlmostSameDir(t1, t2)

        poles = [
            [0, 0],
            [1, 0],
            [1, 1],
            [2, 1],
        ]
        bez = CreateBezier.from_poles(poles)
        u = 0.5
        l = CreateLine.tangent_to_curve(bez, u)
        p1 = gp_Pnt2d()
        p2 = gp_Pnt2d()
        t1 = gp_Vec2d()
        t2 = gp_Vec2d()
        bez.D1(u, p1, t1)
        l.D1(0, p2, t2)
        self.assertAlmostSameCoord(p1, p2)
        self.assertAlmostSameDir(t1, t2)

    def test_normal_to_curve(self):
        poles = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [2, 1, 0],
        ]
        bez = CreateBezier.from_poles(poles)
        u = 0.2
        l = CreateLine.normal_to_curve(bez, u, [0, 0, 1])
        p1 = gp_Pnt()
        p2 = gp_Pnt()
        t1 = gp_Vec()
        t2 = gp_Vec()
        bez.D1(u, p1, t1)
        l.D1(0, p2, t2)
        self.assertAlmostSameCoord(p1, p2)
        self.assertAlmostSameDir(t1, t2.Crossed(gp_Vec(0, 0, -1)))

        poles = [
            [0, 0],
            [1, 0],
            [1, 1],
            [2, 1],
        ]
        bez = CreateBezier.from_poles(poles)
        u = 0.5
        l = CreateLine.normal_to_curve(bez, u)
        p1 = gp_Pnt2d()
        p2 = gp_Pnt2d()
        t1 = gp_Vec2d()
        t2 = gp_Vec2d()
        bez.D1(u, p1, t1)
        l.D1(0, p2, t2)
        self.assertAlmostSameCoord(p1, p2)
        self.assertAlmostSameDir(t1, t2.Rotated(-pi / 2))

    def test_from_point_and_direction(self):
        line3d = CreateLine.from_point_and_direction([0, -1, 0], [0, 1, 0])
        self.assertAlmostSameCoord(line3d.Position().Location(), [0, -1, 0])
        self.assertAlmostSameDir(line3d.Position().Direction(), [0, 2, 0])

        line2d = CreateLine.from_point_and_direction([0, -1], [0, 1])
        self.assertAlmostSameCoord(line2d.Position().Location(), [0, -1])
        self.assertAlmostSameDir(line2d.Position().Direction(), [0, 2])

        with self.assertRaises(TypeError):
            CreateLine.from_point_and_direction([0, -1], [0, 1, 0.])

    def test_through_2_points(self):
        line3d = CreateLine.through_2_points([0, -1, 0], [0, 1, 0])
        self.assertAlmostSameCoord(line3d.Position().Location(), [0, -1, 0])
        self.assertAlmostSameDir(line3d.Position().Direction(), [0, 2, 0])

        line2d = CreateLine.through_2_points([0, -1], [0, 1])
        self.assertAlmostSameCoord(line2d.Position().Location(), [0, -1])
        self.assertAlmostSameDir(line2d.Position().Direction(), [0, 2])

        with self.assertRaises(TypeError):
            CreateLine.through_2_points([0, -1], [0, 1, 0.])

    def test_between_2_points(self):
        line3d = CreateLine.between_2_points([0, -1, 0], [0, 1, 0])
        self.assertAlmostSameCoord(line3d.StartPoint(), [0, -1, 0])
        self.assertAlmostSameCoord(line3d.EndPoint(), [0, 1, 0])
        self.assertAlmostSameDir(line3d.DN(0., 1), [0, 2, 0])
        self.assertAlmostSameDir(line3d.DN(1., 1), [0, 2, 0])

        line2d = CreateLine.between_2_points([-1, -1], [1, 1])
        self.assertAlmostSameCoord(line2d.StartPoint(), [-1, -1])
        self.assertAlmostSameCoord(line2d.EndPoint(), [1, 1])
        self.assertAlmostSameDir(line2d.DN(0., 1), [1, 1])
        self.assertAlmostSameDir(line2d.DN(1., 1), [1, 1])

        with self.assertRaises(TypeError):
            CreateLine.between_2_points([0, -1], [0, 1, 0.])

    def test_between_2_curves_at_position(self):
        bezier1 = CreateBezier.from_poles([[100, 100, 100], [200, 200, 200], [300, 300, 300]])
        bezier2 = CreateBezier.from_poles([[10, 10, 10], [20, 20, 20], [30, 30, 30]])
        segment = CreateLine.between_2_curves_at_positions(bezier1, bezier2, 1., 0.)

        self.assertIsInstance(segment, Geom_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (300, 300, 300))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (10, 10, 10))

        bezier1_2d = CreateBezier.from_poles([[100, 100], [200, 200], [300, 300]])
        bezier2_2d = CreateBezier.from_poles([[10, 10], [20, 20], [30, 30]])
        segment = CreateLine.between_2_curves_at_positions(bezier1_2d, bezier2_2d, 1., 0.)

        self.assertIsInstance(segment, Geom2d_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (300, 300))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (10, 10))

        with self.assertRaises(TypeError):
            CreateLine.between_2_curves_at_positions(bezier1, bezier2_2d, 1., 0.)

    def test_between_2_curves_starts(self):
        bezier1 = CreateBezier.from_poles([[100, 100, 100], [200, 200, 200], [300, 300, 300]])
        bezier2 = CreateBezier.from_poles([[10, 10, 10], [20, 20, 20], [30, 30, 30]])
        segment = CreateLine.between_2_curves_starts(bezier1, bezier2)

        self.assertIsInstance(segment, Geom_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (100, 100, 100))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (10, 10, 10))

        bezier1_2d = CreateBezier.from_poles([[100, 100], [200, 200], [300, 300]])
        bezier2_2d = CreateBezier.from_poles([[10, 10], [20, 20], [30, 30]])
        segment = CreateLine.between_2_curves_starts(bezier1_2d, bezier2_2d)

        self.assertIsInstance(segment, Geom2d_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (100, 100))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (10, 10))

        with self.assertRaises(TypeError):
            CreateLine.between_2_curves_starts(bezier1, bezier2_2d)

    def test_between_2_curves_ends(self):
        bezier1 = CreateBezier.from_poles([[100, 100, 100], [200, 200, 200], [300, 300, 300]])
        bezier2 = CreateBezier.from_poles([[10, 10, 10], [20, 20, 20], [30, 30, 30]])
        segment = CreateLine.between_2_curves_ends(bezier1, bezier2)

        self.assertIsInstance(segment, Geom_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (300, 300, 300))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (30, 30, 30))

        bezier1_2d = CreateBezier.from_poles([[100, 100], [200, 200], [300, 300]])
        bezier2_2d = CreateBezier.from_poles([[10, 10], [20, 20], [30, 30]])
        segment = CreateLine.between_2_curves_ends(bezier1_2d, bezier2_2d)

        self.assertIsInstance(segment, Geom2d_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (300, 300))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (30, 30))

        with self.assertRaises(TypeError):
            CreateLine.between_2_curves_ends(bezier1, bezier2_2d)

    def test_between_point_and_curve_at_position(self):
        bezier2d = CreateBezier.from_poles([[0, 200], [200, 300], [300, 400]])
        point = CreatePoint.as_point((0., -10.))
        segment = CreateLine.between_point_and_curve_at_position(point, gp_Dir2d(0., 1.), bezier2d)
        self.assertIsInstance(segment, Geom2d_TrimmedCurve)
        self.assertAlmostSameCoord(segment.StartPoint().Coord(), (0., -10.))
        self.assertAlmostSameCoord(segment.EndPoint().Coord(), (0., 200.))
