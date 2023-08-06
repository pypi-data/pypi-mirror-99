from math import pi

from OCC.Core.Geom import Geom_Curve

from pyoccad.create import CreateBox, CreateBSpline, CreateCoordSystem
from pyoccad.tests import TestCase
from pyoccad.transform import Rotate


class RotateTest(TestCase):

    def test_around_x(self):
        spline = CreateBSpline.from_points(((0., 0., 0), (1., 2., 3.)))

        result = Rotate.around_x(spline, pi / 2)
        self.assertAlmostSameCoord(spline.EndPoint(), (1., -3., 2.))
        self.assertIsNone(result)

        result = Rotate.around_x(spline, pi / 2, inplace=False)
        self.assertIsInstance(result, Geom_Curve)
        self.assertAlmostSameCoord(spline.EndPoint(), (1., -3., 2.))
        self.assertAlmostSameCoord(result.EndPoint(), (1., -2., -3.))

    def test_around_y(self):
        spline = CreateBSpline.from_points(((0., 0., 0), (1., 2., 3.)))

        result = Rotate.around_y(spline, pi / 2)
        self.assertAlmostSameCoord(spline.EndPoint(), (3., 2., -1))
        self.assertIsNone(result)

        result = Rotate.around_y(spline, pi / 2, inplace=False)
        self.assertIsInstance(result, Geom_Curve)
        self.assertAlmostSameCoord(spline.EndPoint(), (3., 2., -1))
        self.assertAlmostSameCoord(result.EndPoint(), (-1., 2., -3.))

    def test_around_z(self):
        spline = CreateBSpline.from_points(((0., 0., 0), (1., 2., 3.)))

        result = Rotate.around_z(spline, pi / 2)
        self.assertAlmostSameCoord(spline.EndPoint(), (-2., 1., 3.))
        self.assertIsNone(result)

        result = Rotate.around_z(spline, pi / 2, inplace=False)
        self.assertIsInstance(result, Geom_Curve)
        self.assertAlmostSameCoord(spline.EndPoint(), (-2., 1., 3.))
        self.assertAlmostSameCoord(result.EndPoint(), (-1., -2., 3.))

    def test_between_coord_systems(self):
        spline = CreateBSpline.from_points(((0., 0., 0), (1., 2., 3.)))
        coord_system1 = CreateCoordSystem.from_location_and_directions((0, 0, 0), (1, 0, 0), (0, 0, 1))
        coord_system2 = CreateCoordSystem.from_location_and_directions((0, 0, 0), (0, 0, -1), (1, 0, 0))

        result = Rotate.between_coord_systems(spline, coord_system1, coord_system2)
        self.assertAlmostSameCoord(spline.EndPoint(), (3., 2., -1))
        self.assertIsNone(result)

        result = Rotate.between_coord_systems(spline, coord_system1, coord_system2, inplace=False)
        self.assertIsInstance(result, Geom_Curve)
        self.assertAlmostSameCoord(spline.EndPoint(), (3., 2., -1))
        self.assertAlmostSameCoord(result.EndPoint(), (-1., 2., -3.))

        with self.assertRaises(TypeError):
            Rotate.between_coord_systems(spline, coord_system1, (0., 2.))
