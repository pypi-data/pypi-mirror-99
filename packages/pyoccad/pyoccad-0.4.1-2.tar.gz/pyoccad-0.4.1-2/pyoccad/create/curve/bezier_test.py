import numpy as np
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.Geom2d import Geom2d_BezierCurve
from OCC.Core.gp import (gp_Pnt, gp_Vec, gp_Pnt2d)

from pyoccad.create import CreatePoint, CreateVector, CreateControlPoint, CreateBezier
from pyoccad.tests.testcase import TestCase, tol, angTol


class CreateBezierTest(TestCase):

    def setUp(self):
        self.poles = [gp_Pnt(0, 0, 0),
                      [1, 0, 0],
                      gp_Pnt(1, 1, 0),
                      (2, 1, 0)]

        self.poles2d = [gp_Pnt2d(0, 0),
                        [1, 0],
                        gp_Pnt2d(1, 1),
                        (2, 1)]

    def test_from_poles(self):
        poles, poles2d = self.poles, self.poles2d
        bez = CreateBezier.from_poles(poles)
        self.assertIsInstance(bez, Geom_BezierCurve)

        p = gp_Pnt()
        t = gp_Vec()
        bez.D1(bez.FirstParameter(), p, t)
        alpha = t.Angle(CreateVector.from_2_points(poles[0], poles[1]))
        self.assertAlmostEqual(alpha, 0., delta=angTol)

        bez.D1(bez.LastParameter(), p, t)
        alpha = t.Angle(CreateVector.from_2_points(poles[-2], poles[-1]))
        self.assertAlmostEqual(alpha, 0., delta=angTol)

        bez2d = CreateBezier.from_poles(poles2d)
        self.assertIsInstance(bez2d, Geom2d_BezierCurve)

        weights = [0.1, 1, 1.2, 0.8]
        bez = CreateBezier.from_poles(poles, weights)
        for i, w in enumerate(weights):
            self.assertAlmostSameCoord(bez.Pole(i + 1), CreatePoint.as_point(poles[i]))
            self.assertEqual(bez.Weight(i + 1), w)

        with self.assertRaises(TypeError):
            CreateBezier.from_poles(True)
        with self.assertRaises(RuntimeError):
            CreateBezier.from_poles(poles, (1., 2.))
        with self.assertRaises(TypeError):
            CreateBezier.from_poles(poles, True)

    def test_from_control_points(self):
        bez = CreateBezier.from_control_points([CreateControlPoint.from_point((0.1, 0., 0.), (1., 0., 0.)),
                                                CreateControlPoint.from_point((1., 1., 0.), (0., 0.5, 0.))])
        p = gp_Pnt()
        t = gp_Vec()

        self.assertIsInstance(bez, Geom_BezierCurve)
        self.assertEqual(4, bez.NbPoles())

        bez.D1(bez.FirstParameter(), p, t)
        self.assertAlmostSameCoord(p, (0.1, 0., 0.))
        self.assertAlmostSameCoord(t, (1, 0., 0.))

        bez.D1(bez.LastParameter(), p, t)
        self.assertAlmostSameCoord(p, (1., 1., 0.))
        self.assertAlmostSameCoord(t, (0., 0.5, 0.))

        with self.assertRaises(TypeError):
            CreateBezier.from_control_points([gp_Pnt(0, 0, 0), [1, 0, 0]])

        with self.assertRaises(NotImplementedError):
            CreateBezier.from_control_points([CreateControlPoint.from_point()] * 3)

        with self.assertRaises(NotImplementedError):
            CreateBezier.from_control_points([CreateControlPoint.from_point(d2=(1., 1., 1.))] * 2)

    def test_tangent_c0_continuity(self):
        bez = CreateBezier.tangent_c0_continuity([0, 0, 0],
                                                 (2, 1, 0),  # <- did it on purpose
                                                 [1, 0, 0],
                                                 [1, 0, 1]
                                                 )
        self.assertIsInstance(bez, Geom_BezierCurve)

        p = gp_Pnt()
        t = gp_Vec()
        bez.D1(bez.FirstParameter(), p, t)
        alpha = t.Angle(CreateVector.from_point([1, 0, 0]))
        self.assertAlmostEqual(alpha, 0., delta=angTol)

        self.assertAlmostSameCoord((0., 0., 0.), p.Coord())
        self.assertAlmostSameCoord((1., 0., 0.), t.Coord())

        bez.D1(bez.LastParameter(), p, t)
        self.assertAlmostSameCoord((2., 1., 0.), p.Coord())
        self.assertAlmostSameCoord((1., 0., 1.), t.Coord())

    def test_g1_absolute_tension(self):
        bez = CreateBezier.g1_absolute_tension([0, 0, 0],
                                               (2, 1, 0),  # <- did it on purpose
                                               np.r_[1, 0, 0],
                                               [1, 0, 0],
                                               10, 2
                                               )
        self.assertIsInstance(bez, Geom_BezierCurve)

        p = gp_Pnt()
        t = gp_Vec()
        bez.D1(bez.FirstParameter(), p, t)
        alpha = t.Angle(CreateVector.from_point([1, 0, 0]))
        self.assertAlmostEqual(alpha, 0., delta=angTol)

        self.assertAlmostSameCoord((0., 0., 0.), p.Coord())
        self.assertAlmostSameCoord((10., 0., 0.), t.Coord())

        bez.D1(bez.LastParameter(), p, t)
        self.assertAlmostSameCoord((2., 1., 0.), p.Coord())
        self.assertAlmostSameCoord((2., 0., 0.), t.Coord())

    def test_g1_relative_tension(self):
        bez = CreateBezier.g1_relative_tension([0, 0, 0],
                                               (2, 1, 0),  # <- did it on purpose
                                               np.r_[1, 0, 0],  # <- did it on purpose
                                               [0, 2, 0],
                                               1, 2
                                               )
        self.assertIsInstance(bez, Geom_BezierCurve)

        p = gp_Pnt()
        t = gp_Vec()
        ref = np.sqrt(5)
        bez.D1(bez.FirstParameter(), p, t)
        alpha = t.Angle(CreateVector.from_point([1, 0, 0]))
        self.assertAlmostEqual(alpha, 0., delta=angTol)

        self.assertAlmostSameCoord((0., 0., 0.), p.Coord())
        self.assertAlmostSameCoord((ref, 0., 0.), t.Coord())

        bez.D1(bez.LastParameter(), p, t)
        self.assertAlmostSameCoord((2., 1., 0.), p.Coord())
        self.assertAlmostSameCoord((0., 2. * ref, 0.), t.Coord())

    def test_c1_continuity(self):
        bez = CreateBezier.c1_continuity([0, 0, 0],
                                         (2, 1, 0),  # <- did it on purpose
                                         np.r_[1, 0, 0],  # <- did it on purpose
                                         [0, 2, 0],
                                         )
        self.assertIsInstance(bez, Geom_BezierCurve)

        p = gp_Pnt()
        t = gp_Vec()
        bez.D1(bez.FirstParameter(), p, t)
        alpha = t.Angle(CreateVector.from_point([1, 0, 0]))
        self.assertAlmostEqual(alpha, 0., delta=angTol)

        self.assertAlmostSameCoord((0., 0., 0.), p.Coord())
        self.assertAlmostSameCoord((1., 0., 0.), t.Coord())

        bez.D1(bez.LastParameter(), p, t)
        self.assertAlmostSameCoord((2., 1., 0.), p.Coord())
        self.assertAlmostSameCoord((0., 2., 0.), t.Coord())

    def test_c1_connecting_curves(self):
        bez1 = CreateBezier.from_poles([[0., 0., 0.], [0.1, 0., 0.], [0.5, 0.3, 0.]])
        bez2 = CreateBezier.from_poles([[2.3, .8, 0.], [2.5, 1., 0.], [3., 1., 0.]])
        bez3 = CreateBezier.c1_connecting_curves_end_start(bez1, bez2)

        v1 = bez1.DN(bez1.LastParameter(), 1)
        v2 = bez2.DN(bez2.FirstParameter(), 1)
        v1_c = bez3.DN(bez3.FirstParameter(), 1)
        v2_c = bez3.DN(bez3.LastParameter(), 1)

        self.assertAlmostSameCoord(v1, v1_c)
        self.assertAlmostSameCoord(v2, v2_c)

        u1 = 0.3
        u2 = 0.1
        bez3 = CreateBezier.c1_connecting_curves(bez1, bez2, u1, u2)
        v1 = bez1.DN(u1, 1)
        v2 = bez2.DN(u2, 1)
        v1_c = bez3.DN(bez3.FirstParameter(), 1)
        v2_c = bez3.DN(bez3.LastParameter(), 1)

        self.assertAlmostSameCoord(v1, v1_c)
        self.assertAlmostSameCoord(v2, v2_c)

        bez3 = CreateBezier.connecting_curves(bez1, bez2, u1, u2, 1., 1.)
        v1 = bez1.Value(u1)
        v2 = bez2.Value(u2)
        v1_c = bez3.Value(bez3.FirstParameter())
        v2_c = bez3.Value(bez3.LastParameter())

        self.assertAlmostSameCoord(v1, v1_c)
        self.assertAlmostSameCoord(v2, v2_c)
