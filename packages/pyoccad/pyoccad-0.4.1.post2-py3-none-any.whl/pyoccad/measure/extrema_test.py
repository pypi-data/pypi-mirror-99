from OCC.Core.BRepAdaptor import BRepAdaptor_Surface

from pyoccad.create.curve.line import CreateLine
from pyoccad.create.curve.bspline import CreateBSpline
from pyoccad.create.direction import CreateDirection
from pyoccad.create.plane import CreatePlane
from pyoccad.create.point import CreatePoint
from pyoccad.create.surface.face import CreateFace
from pyoccad.measure import MeasureExtrema
from pyoccad.tests.testcase import TestCase, tol

Ox = CreateDirection.ox()
Oy = CreateDirection.oy()
Oz = CreateDirection.oz()


class MeasureExtremaTest(TestCase):

    def test__get_extremum_index(self):
        self.assertEqual(3, MeasureExtrema._get_extremum_index([10, 9, 8, 15], use_smallest=True))
        self.assertEqual(4, MeasureExtrema._get_extremum_index([10, 9, 8, 15], use_smallest=False))

    def test_between_2_curves(self):
        bs1 = CreateBSpline.from_points([[-1, 1, 0], [0, 0.2, 0], [1, 1, 0]])
        line1 = CreateLine.from_point_and_direction([0., -1, 0], [0., 1, 0])
        u1, u2, p1, p2 = MeasureExtrema.between_2_curves(bs1, line1, True, tol)
        self.assertAlmostSameCoord(p1, (0., 0.2, 0.))

        bs2 = CreateBSpline.from_points([[-1, 1, 0], [0, 1, 0], [1, 1, 0]])
        line2 = CreateLine.from_point_and_direction([100, -1, 0], [0, 1, 0])
        u1, u2, p1, p2 = MeasureExtrema.between_2_curves(bs2, line2, True, tol)
        self.assertAlmostEqualValues(u1, 1)
        self.assertAlmostEqualValues(u2, 2)
        self.assertAlmostSameCoord(p1, (1., 1, 0.))
        self.assertAlmostSameCoord(p2, (100., 1, 0.))

        with self.assertRaises(TypeError):
            bspline_2d = CreateBSpline.from_points([[-1, 1], [0, 0.2], [1, 1]])
            MeasureExtrema.between_2_curves(bspline_2d, line2, True, tol)

    def test_between_point_and_curve(self):
        bs1 = CreateBSpline.from_points([[-1, 1, 1], [0, 0, 0], [1, 1, -1]])
        p = CreatePoint.as_point([0, 0, 0])
        u, pc = MeasureExtrema.between_point_and_curve(p, bs1, True, tol)
        self.assertAlmostSameCoord(p, pc)
        self.assertAlmostEqualValues(u, 0.5)

        bs1 = CreateBSpline.from_points([[-1, 1], [0, 0], [1, 1]])
        p = CreatePoint.as_point([0, 0])
        u, pc = MeasureExtrema.between_point_and_curve(p, bs1, True, tol)
        self.assertAlmostSameCoord(p, pc)
        self.assertAlmostEqualValues(u, 0.5)

        with self.assertRaises(TypeError):
            MeasureExtrema.between_point_and_curve(CreatePoint.as_point([0, 0, 0]), bs1, True, tol)

    def test_between_point_and_surface(self):
        s = BRepAdaptor_Surface(CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 1, 1))
        p = CreatePoint.as_point([0.25, 0.5, 0])
        u, v, ps = MeasureExtrema.between_point_and_surface(p, s, True, tol)
        self.assertAlmostEqualValues(u, 0.25)
        self.assertAlmostEqualValues(v, 0.5)
        self.assertAlmostSameCoord(p, ps)

    def test_between_curve_and_surface(self):
        s = BRepAdaptor_Surface(CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 1, 1))
        bs1 = CreateBSpline.from_points([[1, 1, 1], [0.5, 0.5, 0], [0, 0, -1]])
        uc, us, vs, pc, ps = MeasureExtrema.between_curve_and_surface(bs1, s, tol)
        self.assertAlmostEqualValues(uc, 0.5)
        self.assertAlmostEqualValues(us, 0.5)
        self.assertAlmostEqualValues(vs, 0.5)
        self.assertAlmostSameCoord(pc, ps)
        self.assertAlmostSameCoord(ps, (0.5, 0.5, 0.))

        s = BRepAdaptor_Surface(CreateFace.from_plane_and_sizes(CreatePlane.zox(), 1, 1))
        bs2 = CreateBSpline.from_points([[-1, 1, 0], [0, 0.2, 0], [1, 1, 0]])
        uc, us, vs, pc, ps = MeasureExtrema.between_curve_and_surface(bs2, s, True, tol)
        self.assertAlmostEqualValues(uc, 0.5)
        self.assertAlmostEqualValues(us, 0.)
        self.assertAlmostEqualValues(vs, 0.)
        self.assertAlmostSameCoord(pc, (0., 0.2, 0.))
        self.assertAlmostSameCoord(ps, (0., 0., 0.))
