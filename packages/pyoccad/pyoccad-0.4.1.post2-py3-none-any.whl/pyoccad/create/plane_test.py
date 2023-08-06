from OCC.Core.gp import gp_Pnt

from pyoccad.create.axis import CreateAxis
from pyoccad.create.curve.bezier import CreateBezier
from pyoccad.create.direction import CreateDirection
from pyoccad.create.plane import CreatePlane
from pyoccad.tests.testcase import TestCase


class CreatePlaneTest(TestCase):

    def test_xpy(self):
        plane = CreatePlane.xpy(gp_Pnt(1, 1, 1))
        self.assertAlmostSameCoord(plane.Location(), (1, 1, 1))
        self.assertAlmostSameDir(plane.Position().Direction(), (0, 0, 1))

    def test_zpx(self):
        plane = CreatePlane.zpx(gp_Pnt(1, 1, 1))
        self.assertAlmostSameCoord(plane.Location(), (1, 1, 1))
        self.assertAlmostSameDir(plane.Position().Direction(), (0, 1, 0))

    def test_ypz(self):
        plane = CreatePlane.ypz(gp_Pnt(1, 1, 1))
        self.assertAlmostSameCoord(plane.Location(), (1, 1, 1))
        self.assertAlmostSameDir(plane.Position().Direction(), (1, 0, 0))

    def test_xoy(self):
        plane = CreatePlane.xoy()
        self.assertAlmostSameCoord(plane.Location(), (0, 0, 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (0, 0, 1))

    def test_zox(self):
        plane = CreatePlane.zox()
        self.assertAlmostSameCoord(plane.Location(), (0, 0, 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (0, 1, 0))

    def test_yoz(self):
        plane = CreatePlane.yoz()
        self.assertAlmostSameCoord(plane.Location(), (0, 0, 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (1, 0, 0))

    def test_normal_to_curve_at_position(self):
        bezier = CreateBezier.from_poles(((-1, 0, 0), (0, 1, 0), (1, 0, 0)))
        plane = CreatePlane.normal_to_curve_at_position(bezier, 0.5)
        self.assertAlmostSameCoord(plane.Location(), (0, 0.5, 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (1, 0, 0))
        self.assertAlmostSameDir(plane.Position().XDirection(), (0, 0, 1))
        self.assertAlmostSameDir(plane.Position().YDirection(), (0, -1, 0))

    def test_normal_to_curve_at_fraction(self):
        bezier = CreateBezier.from_poles(((-1, 0, 0), (0, 1, 0), (1, 0, 0)))
        plane = CreatePlane.normal_to_curve_at_fraction(bezier, 0.5)
        self.assertAlmostSameCoord(plane.Location(), (0, 0.5, 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (1, 0, 0))
        self.assertAlmostSameDir(plane.Position().XDirection(), (0, 0, 1))
        self.assertAlmostSameDir(plane.Position().YDirection(), (0, -1, 0))

    def test_normal_to_curve_with_xdir(self):
        bezier = CreateBezier.from_poles(((-1, 0, 0), (0, 1, 0), (1, 0, 0)))
        plane = CreatePlane.normal_to_curve_with_xdir(bezier, 0.5, CreateDirection.y_dir())
        self.assertAlmostSameCoord(plane.Location(), (0, 0.5, 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (1, 0, 0))
        self.assertAlmostSameDir(plane.Position().XDirection(), (0, 1, 0))
        self.assertAlmostSameDir(plane.Position().YDirection(), (0, 0, 1))

    def test_from_axis(self):
        plane = CreatePlane.from_axis(CreateAxis.oy())
        self.assertAlmostSameCoord(plane.Location(), (0, 0., 0))
        self.assertAlmostSameDir(plane.Position().Direction(), (0, 1, 0))
