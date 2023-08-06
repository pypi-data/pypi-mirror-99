from math import sqrt, pi

from OCC.Core.Geom import Geom_Ellipse
from OCC.Core.gp import gp_Pnt

from pyoccad.create.curve.ellipse import CreateEllipse
from pyoccad.create.direction import CreateDirection
from pyoccad.create.point import CreatePoint
from pyoccad.tests.testcase import TestCase


class CreateEllipseTest(TestCase):

    @staticmethod
    def build_ellipse():
        center = CreatePoint.as_point((1., 2., 3.))
        normal_direction = CreateDirection.as_direction((0., 0., 1.))
        major_axis_direction = CreateDirection.as_direction((0., 1., 0.))

        ellipse = CreateEllipse.from_center_directions_radii(center,
                                                             (normal_direction, major_axis_direction),
                                                             (5., 10.))
        return ellipse

    def test_from_center_directions_radii(self):
        ellipse = CreateEllipseTest.build_ellipse()

        self.assertIsInstance(ellipse, Geom_Ellipse)
        self.assertEqual(10., ellipse.MajorRadius())
        self.assertEqual(5., ellipse.MinorRadius())
        self.assertAlmostEqual(sqrt(1 - 0.5**2), ellipse.Eccentricity())
        self.assertTrue(ellipse.IsClosed())

        point_ = gp_Pnt()
        ellipse.D0(0., point_)
        self.assertAlmostSameCoord(gp_Pnt(1., 12., 3.), point_)
        ellipse.D0(pi / 2., point_)
        self.assertAlmostSameCoord(gp_Pnt(-4., 2., 3.), point_)
        ellipse.D0(pi, point_)
        self.assertAlmostSameCoord(gp_Pnt(1., -8., 3.), point_)
        ellipse.D0(3 * pi / 2., point_)
        self.assertAlmostSameCoord(gp_Pnt(6., 2., 3.), point_)
