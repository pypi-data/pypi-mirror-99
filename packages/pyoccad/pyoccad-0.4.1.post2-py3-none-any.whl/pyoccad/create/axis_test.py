from OCC.Core.gp import gp_Dir, gp_Dir2d, gp_Ax1, gp_Ax2d

from pyoccad.create import CreateAxis, CreatePoint, CreateDirection
from pyoccad.tests.testcase import TestCase

Ox = gp_Dir(1, 0, 0)
Oy = gp_Dir(0, 1, 0)
Oz = gp_Dir(0, 0, 1)


class TestAxis(TestCase):

    def test_as_axis(self):
        location = CreatePoint.as_point((0., 10., 20.))
        direction = CreateDirection.as_direction((0., 1., 0.))
        axis = CreateAxis.as_axis((location, direction))
        self.assertIsInstance(axis, gp_Ax1)
        self.assertAlmostSameCoord(axis.Location(), location)
        self.assertAlmostSameDir(axis.Direction(), direction)

        location2d = CreatePoint.as_point((0., 10.))
        direction2d = CreateDirection.as_direction((0., 1.))
        axis2d = CreateAxis.as_axis((location2d, direction2d))
        self.assertIsInstance(axis2d, gp_Ax2d)
        self.assertAlmostSameCoord(axis2d.Location(), location2d)
        self.assertAlmostSameDir(axis2d.Direction(), direction2d)

        with self.assertRaises(TypeError):
            CreateAxis.as_axis((location2d))

    def test_base_axes(self):
        self.assertAlmostSameCoord(CreateAxis.ox().Location(), (0., 0., 0.))
        self.assertAlmostSameDir(CreateAxis.ox().Direction(), Ox)
        self.assertAlmostSameCoord(CreateAxis.oy().Location(), (0., 0., 0.))
        self.assertAlmostSameDir(CreateAxis.oy().Direction(), Oy)
        self.assertAlmostSameCoord(CreateAxis.oz().Location(), (0., 0., 0.))
        self.assertAlmostSameDir(CreateAxis.oz().Direction(), Oz)

    def test_from_location_and_direction(self):
        p = CreatePoint.as_point([10, 20, 30])

        px = CreateAxis.from_location_and_direction(p, (1, 0, 0))
        self.assertAlmostSameCoord(px.Location(), p)
        self.assertAlmostSameDir(px.Direction(), Ox)

        py = CreateAxis.from_location_and_direction(p, (0, 1, 0))
        self.assertAlmostSameCoord(py.Location(), p)
        self.assertAlmostSameDir(py.Direction(), Oy)

        pz = CreateAxis.from_location_and_direction(p, (0, 0, 1))
        self.assertAlmostSameCoord(pz.Location(), p)
        self.assertAlmostSameDir(pz.Direction(), Oz)

        p = CreatePoint.as_point([10, 30])
        px = CreateAxis.from_location_and_direction(p, (1, 0))
        self.assertAlmostSameCoord(px.Location(), p)
        self.assertAlmostSameDir(px.Direction(), gp_Dir2d(1, 0))

        with self.assertRaises(TypeError):
            CreateAxis.from_location_and_direction(p, (1, 0, 0))
