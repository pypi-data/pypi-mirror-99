from pyoccad.create.axis import CreateAxis
from pyoccad.create.coord_system import CreateCoordSystem, CreateUnsignedCoordSystem
from pyoccad.measure.coord_system import MeasureCoordSystem
from pyoccad.tests.testcase import TestCase


class MeasureCoordSystemTest(TestCase):

    def test_dimension(self):
        coord_system = CreateCoordSystem.oz()
        self.assertEqual(3, MeasureCoordSystem.dimension(coord_system))
        coord_system = CreateCoordSystem.from_location_and_directions((0., 10., 20.),
                                                                      (0., 1., 0.),
                                                                      (0., 0., 1.))
        self.assertEqual(3, MeasureCoordSystem.dimension(coord_system))
        coord_system = CreateUnsignedCoordSystem.from_location_and_directions((0., 10., 20.),
                                                                              (0., 1., 0.),
                                                                              (0., 0., 1.))
        self.assertEqual(3, MeasureCoordSystem.dimension(coord_system))

        coord_system = CreateCoordSystem.from_location_and_directions((0., 10.),
                                                                      (0., 1.),
                                                                      (1., 0.))
        self.assertEqual(2, MeasureCoordSystem.dimension(coord_system))

        with self.assertRaises(TypeError):
            MeasureCoordSystem.dimension(((0., 10.), (0., 1., 10.), (0., 1.)))

        with self.assertRaises(TypeError):
            MeasureCoordSystem.dimension(CreateAxis.oz())
