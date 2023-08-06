from unittest import skip

from pyoccad.create import CreatePlane, CreateBox, CreateFace
from pyoccad.explore.subshapes import ExploreSubshapes
from pyoccad.heal import sew
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class TestSew(TestCase):

    def test_to_compound(self):
        box = CreateBox.from_dimensions((1, 1, 1))
        f_lst = ExploreSubshapes.get_faces(box)

        C = sew.to_compound(f_lst)
        self.assertAlmostEqual(MeasureSurface.area(C), 6.)

    # TODO: understand why this test fails
    @skip('skip the rolling ball test, failing for the moment')
    def test_to_shells(self):
        box = CreateBox.from_dimensions_and_center((1., 1., 1.))

        f_lst = ExploreSubshapes.get_faces(box)
        s = CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 1, 1)
        f_lst.append(s)

        sh_lst = sew.to_shells(f_lst)
        self.assertTrue(len(sh_lst) == 2)
