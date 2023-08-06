from pyoccad.create import CreateBox, CreateTranslation
from pyoccad.tests import TestCase
from pyoccad.transform import Move
from pyoccad.measure import solid


class MoveTest(TestCase):

    def test_using_transformation(self):
        box = CreateBox.from_dimensions_and_center((1., 1., 1.))
        translation = CreateTranslation.from_vector((1, 2, 3))
        self.assertAlmostSameCoord(solid.center(box), (0, 0, 0))

        Move.using_transformation(box, translation)
        self.assertAlmostSameCoord(solid.center(box), (1, 2, 3))


