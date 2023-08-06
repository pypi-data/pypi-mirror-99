from pyoccad.create import CreateBox
from pyoccad.measure import solid
from pyoccad.tests import TestCase
from pyoccad.transform import Translate


class TranslateTest(TestCase):

    def test_from_vector(self):
        box = CreateBox.from_dimensions_and_center((1., 1., 1.))
        self.assertAlmostSameCoord(solid.center(box), (0, 0, 0))

        Translate.from_vector(box, (10, 20, 30))
        self.assertAlmostSameCoord(solid.center(box), (10, 20, 30))


