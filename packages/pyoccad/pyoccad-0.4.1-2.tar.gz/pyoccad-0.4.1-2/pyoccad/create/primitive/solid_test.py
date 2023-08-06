from math import pi

from OCC.Core.gp import gp_Pnt

from pyoccad.create import CreateShell, CreateSolid, CreateBox, CreateSphere, CreateCone
from pyoccad.explore.subshapes import ExploreSubshapes
from pyoccad.measure import solid as ms
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class CreateBoxTest(TestCase):

    def test_box_from_dims(self):
        b1 = CreateBox.from_dimensions((1, 2, 3))
        self.assertAlmostEqualValues(ms.volume(b1), 6.)

    def test_box_from_dims_and_center(self):
        box = CreateBox.from_dimensions_and_center((1, 1, 1))
        self.assertAlmostEqualValues(ms.volume(box), 1.)
        cg = ms.center(box)
        self.assertAlmostSameCoord(cg.Coord(), gp_Pnt())


class CreatConeTest(TestCase):

    def test_from_base_and_dir(self):
        c1 = CreateCone.from_base_and_dir([0, 0, 0], [1, 0, 0], 1)
        self.assertAlmostEqualValues(ms.volume(c1), pi / 3)


class CreatSphereTest(TestCase):

    def test_from_radius_and_center(self):
        s1 = CreateSphere.from_radius_and_center(1., [1, 1, 2])
        self.assertAlmostEqualValues(ms.volume(s1), 4 * pi / 3)
        cg = ms.center(s1)
        self.assertAlmostNullValue(cg.Distance(gp_Pnt(1, 1, 2)))


class CreateSolidTest(TestCase):

    def test_from_shell(self):
        box = CreateBox.from_dimensions((1, 1, 1))
        f_lst = ExploreSubshapes.get_faces(box)
        sh = CreateShell.from_faces(f_lst)
        s = CreateSolid.from_shell(sh)
        self.assertAlmostEqualValues(MeasureSurface.area(s), 6.)
