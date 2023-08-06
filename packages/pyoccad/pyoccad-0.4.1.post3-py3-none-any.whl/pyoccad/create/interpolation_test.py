from OCC.Core.Law import Law_Interpol

from pyoccad.create import CreateInterpolation
from pyoccad.tests.testcase import TestCase


class CreateInterpolationTest(TestCase):

    def test_of_points(self):
        container = [[0., 1.], [0.5, 2.], [1., 3.]]
        law_bs = CreateInterpolation.of_points(container)
        self.assertIsInstance(law_bs, Law_Interpol)
        for p in container:
            self.assertAlmostEqualValues(p[1], law_bs.Value(p[0]))
