from pyoccad.create import CreateBezierSurface, CreateBox
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests import testcase


class MeasureSurfaceTest(testcase.TestCase):

    def test_area(self):
        s = CreateBezierSurface.from_poles([[[0, 0, 0], [1, 0, 0]],
                                            [[0, 1, 0], [1, 1, 0]]])
        self.assertAlmostEqualValues(MeasureSurface.area(s), 1.)

    def test_center(self):
        s = CreateBezierSurface.from_poles([[[0, 0, 0], [1, 0, 0]],
                                            [[0, 1, 0], [1, 1, 0]]])
        self.assertAlmostSameCoord(MeasureSurface.center(s), [0.5, 0.5, 0.])

        box = CreateBox.from_dimensions((1, 1, 1))
        self.assertAlmostSameCoord(MeasureSurface.center(box), [0.5, 0.5, 0.5])
