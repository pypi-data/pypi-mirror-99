from pyoccad.create.axis import CreateAxis
from pyoccad.create.coord_system import CreateCoordSystem
from pyoccad.measure.axis import MeasureAxis
from pyoccad.tests.testcase import TestCase


class MeasureAxisTest(TestCase):

    def test_dimension(self):
        axis2d = CreateAxis.from_location_and_direction((0., 0.), (0., 1.))
        self.assertEqual(2, MeasureAxis.dimension(axis2d))

        axis3d = CreateAxis.from_location_and_direction((0., 0., 0.), (0., 1., 0.))
        self.assertEqual(3, MeasureAxis.dimension(axis3d))

        with self.assertRaises(TypeError):
            MeasureAxis.dimension(CreateCoordSystem.oz())
