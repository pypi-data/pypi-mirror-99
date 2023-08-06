from math import pi

from pyoccad.create import CreateLine, CreateCircle
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase
from pyoccad.transform import Filling


class TestFilling(TestCase):

    def test_from_profiles(self):
        l1 = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        l2 = CreateLine.between_2_points([0, 1, 0], [1, 1, 0])
        prf_lst = [l1, l2]
        fill1 = Filling.from_profiles(prf_lst)
        self.assertAlmostEqualValues(MeasureSurface.area(fill1), 1)

        c1 = CreateCircle.from_radius_and_center(1.)
        c2 = CreateCircle.from_radius_and_center(1., [0, 0, 1])
        prf_lst = [c1, c2]
        fill2 = Filling.from_profiles(prf_lst)
        self.assertAlmostEqualValues(MeasureSurface.area(fill2), 2 * pi)

        fill3 = Filling.from_profiles(prf_lst, build_solid=True)
        self.assertAlmostEqualValues(MeasureSurface.area(fill3), 4 * pi)
