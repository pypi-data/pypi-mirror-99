from math import pi

from OCC.Core.Geom import Geom_TrimmedCurve, Geom_Ellipse
from OCC.Core.Geom2d import Geom2d_TrimmedCurve
from OCC.Core.Geom2dAPI import Geom2dAPI_ProjectPointOnCurve
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.gp import (gp_Pnt, gp_Vec, gp_Dir, gp_Ax2, gp_Pnt2d, gp_Vec2d, gp_Dir2d, gp_Ax22d, gp_Elips)

from pyoccad.create.curve.arc import CreateArc
from pyoccad.create.curve.ellipse_test import CreateEllipseTest
from pyoccad.create.point import CreatePoint
from pyoccad.create.coord_system import CreateCoordSystem
from pyoccad.measure import MeasureCurve
from pyoccad.tests.testcase import TestCase, tol, angTol


class CreateArcTest(TestCase):

    def setUp(self):
        self.ax2 = gp_Ax2(gp_Pnt(1, 1, 0), gp_Dir(1, 1, 0), gp_Dir(1, 0, 0))
        self.ax22d = gp_Ax22d(gp_Pnt2d(1, 1), gp_Dir2d(1, 0), gp_Dir2d(0, 1))
        self.a1 = pi / 6
        self.a2 = pi / 2

    def test_from_angles(self):
        ax2, ax22d = self.ax2, self.ax22d
        r = 2.3
        a1, a2 = self.a1, self.a2
        c = CreateArc.from_angles(ax2, r, a1, a2)
        self.assertAlmostEqual(MeasureCurve.length(c), r * abs(a2 - a1), delta=tol)
        d1 = gp_Dir(gp_Vec(ax2.Location(), c.StartPoint()))
        self.assertAlmostEqual(ax2.XDirection().Angle(d1), a1, delta=angTol)
        d2 = gp_Dir(gp_Vec(ax2.Location(), c.EndPoint()))
        self.assertAlmostEqual(ax2.XDirection().Angle(d2), a2, delta=angTol)

        c = CreateArc.from_angles(ax2, r, 0, a1)
        self.assertIsInstance(c, Geom_TrimmedCurve)
        self.assertAlmostEqual(MeasureCurve.length(c), r * abs(a1), delta=tol)
        d1 = gp_Dir(gp_Vec(ax2.Location(), c.StartPoint()))
        self.assertAlmostEqual(ax2.XDirection().Angle(d1), 0, delta=angTol)
        d2 = gp_Dir(gp_Vec(ax2.Location(), c.EndPoint()))
        self.assertAlmostEqual(ax2.XDirection().Angle(d2), a1, delta=angTol)

        ax22d = self.ax22d
        r = 2.3
        a1 = pi / 6
        a2 = pi / 2

        c = CreateArc.from_angles(ax22d, r, a1, a2)
        self.assertAlmostEqual(MeasureCurve.length(c), r * abs(a2 - a1), delta=tol)
        d1 = gp_Dir2d(gp_Vec2d(ax22d.Location(), c.StartPoint()))
        self.assertAlmostEqual(ax22d.XDirection().Angle(d1), a1, delta=angTol)
        d2 = gp_Dir2d(gp_Vec2d(ax22d.Location(), c.EndPoint()))
        self.assertAlmostEqual(ax22d.XDirection().Angle(d2), a2, delta=angTol)

        c = CreateArc.from_angles(ax22d, r, 0., a1)
        self.assertIsInstance(c, Geom2d_TrimmedCurve)
        self.assertAlmostEqual(MeasureCurve.length(c), r * abs(a1), delta=tol)
        d1 = gp_Dir2d(gp_Vec2d(ax22d.Location(), c.StartPoint()))
        self.assertAlmostEqual(ax22d.XDirection().Angle(d1), 0, delta=angTol)
        d2 = gp_Dir2d(gp_Vec2d(ax22d.Location(), c.EndPoint()))
        self.assertAlmostEqual(ax22d.XDirection().Angle(d2), a1, delta=angTol)

        with self.assertRaises(TypeError):
            CreateArc.from_angles(True, r, 0., a1)

    def test_from_3_points(self):
        ax2, ax22d = self.ax2, self.ax22d
        p1 = [0, 1, 2]
        a1, a2 = self.a1, self.a2
        p2 = CreatePoint.as_point(p1).Rotated(ax2.Axis(), a1)
        p3 = CreatePoint.as_point(p1).Rotated(ax2.Axis(), a2)
        c = CreateArc.from_3_points((p1, p2, p3))
        self.assertIsInstance(c, Geom_TrimmedCurve)
        self.assertAlmostEqual(GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(p1), c).LowerDistance(), 0., delta=tol)
        self.assertAlmostEqual(GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(p2), c).LowerDistance(), 0., delta=tol)
        self.assertAlmostEqual(GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(p3), c).LowerDistance(), 0., delta=tol)
        self.assertAlmostEqual(c.StartPoint().Distance(CreatePoint.as_point(p1)), 0., delta=tol)
        self.assertAlmostEqual(c.EndPoint().Distance(CreatePoint.as_point(p3)), 0., delta=tol)

        p1 = [0, 1]
        p2 = CreatePoint.as_point(p1).Rotated(ax22d.Location(), a1)
        p3 = CreatePoint.as_point(p1).Rotated(ax22d.Location(), a2)
        c = CreateArc.from_3_points((p1, p2, p3))
        self.assertIsInstance(c, Geom2d_TrimmedCurve)
        self.assertAlmostEqual(Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(p1), c).LowerDistance(), 0., delta=tol)
        self.assertAlmostEqual(Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(p2), c).LowerDistance(), 0., delta=tol)
        self.assertAlmostEqual(Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(p3), c).LowerDistance(), 0., delta=tol)
        self.assertAlmostEqual(c.StartPoint().Distance(CreatePoint.as_point(p1)), 0., delta=tol)
        self.assertAlmostEqual(c.EndPoint().Distance(CreatePoint.as_point(p3)), 0., delta=tol)

        with self.assertRaises(TypeError):
            CreateArc.from_3_points(([0., 1., 2], p2, p3))
        with self.assertRaises(TypeError):
            CreateArc.from_3_points(True)

    def test_from_ellipse(self):
        geom_ellipse = CreateEllipseTest.build_ellipse()
        self.assertIsInstance(geom_ellipse, Geom_Ellipse)

        coord_system = CreateCoordSystem.as_coord_system(((1., 2., 3.), (0., 1., 0.), (0., 0., 1.)))
        gp_ellipse = gp_Elips(coord_system, 10, 5)
        self.assertIsInstance(gp_ellipse, gp_Elips)

        for ellipse in (geom_ellipse, gp_ellipse):

            ellipse_arc = CreateArc.from_ellipse(ellipse, pi / 4, 3. * pi / 4.)

            self.assertIsInstance(ellipse_arc, Geom_TrimmedCurve)
            self.assertFalse(ellipse_arc.IsClosed())
            self.assertAlmostEqual(pi / 4, ellipse_arc.FirstParameter())
            self.assertAlmostEqual(3. * pi / 4, ellipse_arc.LastParameter())

            point_ = gp_Pnt()
            ellipse_arc.D0(0., point_)
            self.assertAlmostSameCoord(gp_Pnt(1., 12., 3.), point_)
            ellipse_arc.D0(pi / 2., point_)
            self.assertAlmostSameCoord(gp_Pnt(-4., 2., 3.), point_)
            ellipse_arc.D0(pi, point_)
            self.assertAlmostSameCoord(gp_Pnt(1., -8., 3.), point_)
            ellipse_arc.D0(3 * pi / 2., point_)
            self.assertAlmostSameCoord(gp_Pnt(6., 2., 3.), point_)
