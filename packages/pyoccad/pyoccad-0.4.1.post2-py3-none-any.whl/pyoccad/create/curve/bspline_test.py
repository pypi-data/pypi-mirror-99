from math import pi

import numpy as np
from OCC.Core.Geom2dAPI import Geom2dAPI_ProjectPointOnCurve
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.gp import (gp_Pnt, gp_Vec)

from pyoccad.create import CreateBSpline, CreateCircle, CreateEdge, CreateWire, CreatePoint, CreateVector
from pyoccad.measure import MeasureCurve
from pyoccad.tests.testcase import TestCase, tol, angTol


class CreateBSplineTest(TestCase):

    def test_from_points(self):
        points = [
            gp_Pnt(0, 0, 0),
            [1, 0, 0],
            [1, 2, 0],
            np.array([0, 1, -1]),
        ]
        bs = CreateBSpline.from_points(points)

        for point_ in points:
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        points = np.array([
            [0, 0],
            [1, 0],
            [1, 2],
            [0, 1],
        ])
        bs = CreateBSpline.from_points(points)

        for point_ in points:
            d = Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        # bs = CreateBSpline.from_points(points,tol,True) #TODO check what is wrong
        # self.assertTrue( bs.IsPeriodic() )

    def test_from_points_with_params(self):
        points = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 2, 0],
            [0, 1, -1],
        ]
        w = [
            0.,
            0.3,
            0.5,
            1.,
        ]
        bs = CreateBSpline.from_points_with_params(points, w, tol)

        for point_ in points:
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        points = [
            [0, 0],
            [1, 0],
            [1, 2],
            [0, 1],
        ]
        w = np.array([
            0.,
            0.3,
            0.5,
            1.,
        ])
        bs = CreateBSpline.from_points_with_params(points, w, tol)

        for point_ in points:
            d = Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

    def test_from_points_with_smoothing(self):
        points = (
            (0, 0, 0),
            (1, 0, 0),
            (1, 2, 0),
            (0, 1, -1))
        bs = CreateBSpline.from_points_with_smoothing(points, (1., 1., 1.), tol)

        for point_ in points:
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        points = (
            (0, 0),
            (1, 0),
            (1, 2),
            (0, 1))
        bs = CreateBSpline.from_points_with_smoothing(points, (1., 1., 1.), tol)

        for point_ in points:
            d = Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

    def test_from_points_interpolate(self):
        points = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 2, 0],
            [0, 1, -1],
        ]
        bs = CreateBSpline.from_points_interpolate(points, tol)

        for point_ in points:
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        points = [
            [0, 0],
            [1, 0],
            [1, 2],
            [0, 1],
        ]
        bs = CreateBSpline.from_points_interpolate(points, tol)

        for point_ in points:
            d = Geom2dAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

    def test_from_points_interpolate_with_bounds_control(self):
        points = (
            (0, 0, 0),
            (1, 0, 0),
            (1, 2, 0),
            (0, 1, -1))
        t_start = gp_Vec(1, 0, 0)
        t_end = (1, 1, 0)
        bs = CreateBSpline.from_points_interpolate_with_bounds_control(points, (t_start, t_end), tol)

        for point_ in points:
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        p1 = gp_Pnt()
        p2 = gp_Pnt()
        t1 = gp_Vec()
        t2 = gp_Vec()
        bs.D1(bs.FirstParameter(), p1, t1)
        bs.D1(bs.LastParameter(), p2, t2)
        self.assertAlmostEqual(t_start.Angle(t1), 0, delta=angTol)
        self.assertAlmostEqual(CreateVector.from_point(t_end).Angle(t2), 0, delta=angTol)

        bs = CreateBSpline.from_points_interpolate_with_bounds_control(points, (t_start, t_end), tol, False)

        for p in points:
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(p), bs).LowerDistance()
            self.assertAlmostEqual(d, tol, delta=tol)

        self.assertAlmostEqual(t_start.Angle(t1), 0, delta=angTol)
        self.assertAlmostEqual(CreateVector.from_point(t_end).Angle(t2), 0, delta=angTol)

        # self.assertAlmostEqual(tStart.Magnitude(),t1.Magnitude(),delta=tol) #TODO find a way tu get the correct tg
        # self.assertAlmostEqual(vector.from_point(tEnd).Magnitude(),t2.Magnitude(),0,delta=tol)

    def test_from_points_and_tangents_interpolate(self):
        points = [
            [0, 0, 0],
            [1, 0, 0],
            [1, 2, 0],
            [0, 1, -1],
        ]
        tg = [
            [1, 0, 0],
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
        ]

        bs = CreateBSpline.from_points_and_tangents_interpolate(points, tg, tol)

        p = gp_Pnt()
        t = gp_Vec()
        for i, point_ in enumerate(points):
            d = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistance()
            u = GeomAPI_ProjectPointOnCurve(CreatePoint.as_point(point_), bs).LowerDistanceParameter()
            bs.D1(u, p, t)
            self.assertAlmostEqual(d, tol, delta=tol)
            if CreateVector.from_point(tg[i]).Magnitude() > tol:
                self.assertAlmostEqual(CreateVector.from_point(tg[i]).Angle(t), 0, delta=angTol)

        tg2d = [
            [1, 0],
            [0, 0],
            [0, 1],
            [1, 1],
        ]
        with self.assertRaises(TypeError):
            CreateBSpline.from_points_and_tangents_interpolate(points, tg2d, tol)

        with self.assertRaises(AttributeError):
            CreateBSpline.from_points_and_tangents_interpolate(points, ((0., 0., 0.), ), tol)

    def test_from_poles_and_degree(self):
        poles = [[0, 0, 0], [1, 2, 3], [4, 5, 6]]
        bs = CreateBSpline.from_poles_and_degree(poles, 3)
        bs_poles = bs.Poles()
        for i, _ in enumerate(poles):
            self.assertAlmostSameCoord(bs_poles.Value(i + 1), CreatePoint.as_point(poles[i]))

        poles = [[0, 0], [1, 2], [3, 4]]
        bs = CreateBSpline.from_poles_and_degree(poles, 3)
        bs_poles = bs.Poles()
        for i, _ in enumerate(poles):
            self.assertAlmostSameCoord(bs_poles.Value(i + 1), CreatePoint.as_point(poles[i]))

        poles = [[0, 0, 0], [1, 2, 3], [4, 5, 6]]
        bs = CreateBSpline.from_poles_and_degree(poles, 3, True)
        bs_poles = bs.Poles()
        for i, _ in enumerate(poles):
            self.assertAlmostSameCoord(bs_poles.Value(i + 1), CreatePoint.as_point(poles[i]))

        poles = [[0, 0], [1, 2], [3, 4]]
        bs = CreateBSpline.from_poles_and_degree(poles, 3, True)
        bs_poles = bs.Poles()
        for i, _ in enumerate(poles):
            self.assertAlmostSameCoord(bs_poles.Value(i + 1), CreatePoint.as_point(poles[i]))

        poles = [[0, 0, 0], [1, 2, 3], [4, 5, 6]]
        bs = CreateBSpline.from_poles_and_degree(poles, 5)
        bs_poles = bs.Poles()
        for i, _ in enumerate(poles):
            self.assertAlmostSameCoord(bs_poles.Value(i + 1), CreatePoint.as_point(poles[i]))

        poles = [[0, 0, 0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
        bs = CreateBSpline.from_poles_and_degree(poles, 5)
        bs_poles = bs.Poles()
        for i, _ in enumerate(poles):
            self.assertAlmostSameCoord(bs_poles.Value(i + 1), CreatePoint.as_point(poles[i]))

    def test_approximation(self):
        c3d = CreateCircle.from_radius_and_center(1.)
        c2d = CreateCircle.from_radius_and_center(1., [0, 0])
        c3d_approx = CreateBSpline.approximation(c3d, 1e-6)
        self.assertAlmostEqualValues(MeasureCurve.length(c3d_approx), 2 * pi)

        c3d_approx = CreateBSpline.approximation(c3d, 1e-6, curvilinear_abs=True)
        self.assertAlmostEqualValues(MeasureCurve.length(c3d_approx), 2 * pi)

        c2d_approx = CreateBSpline.approximation(c2d, 1e-6)
        self.assertAlmostEqualValues(MeasureCurve.length(c2d_approx), 2 * pi)

        ed = CreateEdge.from_contour(c3d)
        ed_approx = CreateBSpline.approximation(ed, 1e-6)
        self.assertAlmostEqualValues(MeasureCurve.length(ed_approx), 2 * pi)

        w = CreateWire.from_elements([ed])
        w_approx = CreateBSpline.approximation(w, 1e-6)
        self.assertAlmostEqualValues(MeasureCurve.length(w_approx), 2 * pi)
