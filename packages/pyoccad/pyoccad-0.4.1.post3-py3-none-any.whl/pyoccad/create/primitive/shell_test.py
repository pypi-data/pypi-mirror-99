from pyoccad.create import CreateShell, CreateBox
from pyoccad.explore.subshapes import ExploreSubshapes
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class CreateShellTest(TestCase):

    def test_from_faces(self):
        box = CreateBox.from_dimensions((1, 1, 1))
        f_lst = ExploreSubshapes.get_faces(box)
        sh = CreateShell.from_faces(f_lst)
        self.assertAlmostEqualValues(MeasureSurface.area(sh), 6.)
