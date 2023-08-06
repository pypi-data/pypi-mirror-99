from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.gp import gp_Dir

from pyoccad.create import CreateIntersection, CreatePlane, CreatePoint
from pyoccad.create import CreateBSpline, CreateLine, CreateFace
from pyoccad.tests.testcase import TestCase, tol

Ox = gp_Dir(1, 0, 0)
Oy = gp_Dir(0, 1, 0)
Oz = gp_Dir(0, 0, 1)


class CreateIntersectionTest(TestCase):

    def test_between_2_curves(self):
        bs1 = CreateBSpline.from_points([[-1, 1, 0], [0, 0.2, 0], [1, 1, 0]])
        line1 = CreateLine.from_point_and_direction([0., -1, 0], [0., 1, 0])
        p1 = CreateIntersection.between_2_curves(bs1, line1, tol)
        self.assertAlmostSameCoord(p1, (0., 0.2, 0.))

        line2 = CreateLine.from_point_and_direction([1.1, -1, 0], [1.1, 1, 0])
        with self.assertRaises(ArithmeticError):
            CreateIntersection.between_2_curves(bs1, line2, tol)

        with self.assertRaises(TypeError):
            CreateIntersection.between_2_curves(CreateBSpline.from_points([[-1, 1], [0, 0.2], [1, 1]]), line2, tol)

    def test_between_point_and_curve(self):
        bs1 = CreateBSpline.from_points([[-1, 1, 1], [0, 0, 0], [1, 1, -1]])
        p = CreatePoint.as_point([0, 0, 0])
        pc = CreateIntersection.between_point_and_curve(p, bs1, tol)
        self.assertAlmostSameCoord(p, pc)

        bs1 = CreateBSpline.from_points([[-1, 1], [0, 0], [1, 1]])
        p = CreatePoint.as_point([0, 0])
        pc = CreateIntersection.between_point_and_curve(p, bs1, tol)
        self.assertAlmostSameCoord(p, pc)

        with self.assertRaises(TypeError):
            CreateIntersection.between_point_and_curve(CreatePoint.as_point([0, 0, 0]), bs1, tol)

        with self.assertRaises(ArithmeticError):
            CreateIntersection.between_point_and_curve(CreatePoint.as_point([1.1, 0]), bs1, tol)

    def test_between_point_and_surface(self):
        s = BRepAdaptor_Surface(CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 1, 1))
        p = CreatePoint.as_point([0.25, 0.5, 0])
        ps = CreateIntersection.between_point_and_surface(p, s, tol)
        self.assertAlmostSameCoord(p, ps)

        with self.assertRaises(ArithmeticError):
            CreateIntersection.between_point_and_surface(CreatePoint.as_point((0, 0, 0.1)), s, tol)

    def test_between_curve_and_surface(self):
        s = BRepAdaptor_Surface(CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 1, 1))
        bs1 = CreateBSpline.from_points([[1, 1, 1], [0.5, 0.5, 0], [0, 0, -1]])
        p = CreateIntersection.between_curve_and_surface(bs1, s, tol)
        self.assertAlmostSameCoord(p, (0.5, 0.5, 0.))

        s2 = BRepAdaptor_Surface(CreateFace.from_points(((0., 0., 0.), (-0.1, 0., 0.), (-0.1, -0.1, 0.))))
        with self.assertRaises(ArithmeticError):
            CreateIntersection.between_curve_and_surface(bs1, s2, tol)
