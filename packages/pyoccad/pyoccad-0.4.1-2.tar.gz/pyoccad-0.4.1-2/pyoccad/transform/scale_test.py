from OCC.Core.TopoDS import TopoDS_Solid

from pyoccad.create import CreateBox
from pyoccad.measure import solid
from pyoccad.tests import TestCase
from pyoccad.transform import Scale


class ScaleTest(TestCase):

    def test_using_transformation(self):
        box = CreateBox.from_dimensions_and_center((1., 1., 1.))
        self.assertAlmostSameCoord(solid.center(box), (0, 0, 0))
        self.assertAlmostEqual(1, solid.volume(box))

        result = Scale.from_factor(box, 10)
        self.assertAlmostSameCoord(solid.center(box), (0, 0, 0))
        self.assertAlmostEqual(1000, solid.volume(box))
        self.assertIsNone(result)

        result = Scale.from_factor(box, 10, inplace=False)
        self.assertAlmostSameCoord(solid.center(box), (0, 0, 0))
        self.assertAlmostEqual(1000, solid.volume(box))
        self.assertIsInstance(result, TopoDS_Solid)
        self.assertAlmostSameCoord(solid.center(result), (0, 0, 0))
        self.assertAlmostEqual(1000000, solid.volume(result))
