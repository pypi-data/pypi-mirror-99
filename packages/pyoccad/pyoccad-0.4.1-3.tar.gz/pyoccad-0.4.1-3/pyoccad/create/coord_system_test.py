from math import pi

from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax3, gp_Ax22d, gp_Ax2

from pyoccad.create import CreatePoint, CreateAxis, CreateCoordSystem, CreateUnsignedCoordSystem
from pyoccad.tests.testcase import TestCase

Ox = gp_Dir(1, 0, 0)
Oy = gp_Dir(0, 1, 0)
Oz = gp_Dir(0, 0, 1)


class CreateCoordinateSystemTest(TestCase):

    def test_as_coord_system(self):
        center = (10., 20., 30.)
        direction = (0., 1., 0.)
        xdirection = (0., 0., 1.)
        coord_system = CreateCoordSystem.as_coord_system((center, xdirection, direction))
        self.assertIsInstance(coord_system, gp_Ax2)
        self.assertAlmostSameCoord(coord_system.Location(), center)
        self.assertAlmostSameDir(coord_system.Direction(), direction)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection)

        coord_system_ = gp_Ax2(gp_Pnt(*center), gp_Dir(*direction), gp_Dir(*xdirection))
        self.assertIsInstance(coord_system_, gp_Ax2)
        coord_system = CreateCoordSystem.as_coord_system(coord_system_)
        self.assertIsInstance(coord_system, gp_Ax2)
        self.assertAlmostSameCoord(coord_system.Location(), center)
        self.assertAlmostSameDir(coord_system.Direction(), direction)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection)

        coord_system_ = gp_Ax3(gp_Pnt(*center), gp_Dir(*direction), gp_Dir(*xdirection))
        self.assertIsInstance(coord_system_, gp_Ax3)
        coord_system = CreateCoordSystem.as_coord_system(coord_system_)
        self.assertIsInstance(coord_system, gp_Ax2)
        self.assertAlmostSameCoord(coord_system.Location(), center)
        self.assertAlmostSameDir(coord_system.Direction(), direction)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection)

        center2d = (10., 20.)
        direction2d = (1., 0.)
        xdirection2d = (0., 1.)
        coord_system = CreateCoordSystem.as_coord_system((center2d, xdirection2d, direction2d))
        self.assertIsInstance(coord_system, gp_Ax22d)
        self.assertAlmostSameCoord(coord_system.Location(), center2d)
        self.assertAlmostSameDir(coord_system.YDirection(), direction2d)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection2d)

        with self.assertRaises(TypeError):
            CreateCoordSystem.as_coord_system((0., 0.))

    def test_base_coordinate_systems(self):
        ox = CreateCoordSystem.ox()
        self.assertIsInstance(ox, gp_Ax2)
        self.assertAlmostSameCoord(ox.Location(), (0., 0., 0.))
        self.assertAlmostSameDir(ox.Direction(), Ox)

        oy = CreateCoordSystem.oy()
        self.assertIsInstance(oy, gp_Ax2)
        self.assertAlmostSameCoord(oy.Location(), (0., 0., 0.))
        self.assertAlmostSameDir(oy.Direction(), Oy)

        oz = CreateCoordSystem.oz()
        self.assertIsInstance(oz, gp_Ax2)
        self.assertAlmostSameCoord(oz.Location(), (0., 0., 0.))
        self.assertAlmostSameDir(oz.Direction(), Oz)

    def test_rotated_coordinate_systems(self):
        angle = pi / 6.

        self.assertAlmostSameDir(CreateCoordSystem.rotated_ox(angle).Direction(), Ox)
        self.assertAlmostSameDir(CreateCoordSystem.rotated_oy(angle).Direction(), Oy)
        self.assertAlmostSameDir(CreateCoordSystem.rotated_oz(angle).Direction(), Oz)

        self.assertAlmostSameDir(CreateCoordSystem.rotated_ox(angle).XDirection(),
                                 CreateAxis.oy().Rotated(CreateAxis.ox(), angle).Direction())
        self.assertAlmostSameDir(CreateCoordSystem.rotated_oy(angle).XDirection(),
                                 CreateAxis.ox().Rotated(CreateAxis.oy(), angle).Direction())
        self.assertAlmostSameDir(CreateCoordSystem.rotated_oz(angle).XDirection(),
                                 CreateAxis.ox().Rotated(CreateAxis.oz(), angle).Direction())

    def test_from_location_and_directions(self):
        p = CreatePoint.as_point((10, 20, 30))
        coord_system = CreateCoordSystem.from_location_and_directions(p, [1, 0, 0], [0, 1, 0])
        self.assertIsInstance(coord_system, gp_Ax2)
        self.assertAlmostSameCoord(coord_system.Location(), p)
        self.assertAlmostSameDir(coord_system.Direction(), Oy)
        self.assertAlmostSameDir(coord_system.XDirection(), Ox)
        self.assertAlmostSameDir(coord_system.YDirection(), -Oz)

        p = CreatePoint.as_point((10, 30))
        coord_system = CreateCoordSystem.from_location_and_directions(p, [0, 1], [1, 0])
        self.assertIsInstance(coord_system, gp_Ax22d)
        self.assertAlmostSameCoord(coord_system.Location(), p)
        self.assertAlmostSameDir(coord_system.XDirection(), (0, 1))
        self.assertAlmostSameDir(coord_system.YDirection(), (1, 0))

        with self.assertRaises(TypeError):
            CreateCoordSystem.from_location_and_directions(p, [0, 1], [1, 0, 0])


class CreateUnsignedCoordinateSystemTest(TestCase):

    def test_as_coord_system(self):
        center = (10., 20., 30.)
        direction = (0., 1., 0.)
        xdirection = (0., 0., 1.)
        coord_system = CreateUnsignedCoordSystem.as_coord_system((center, xdirection, direction))
        self.assertIsInstance(coord_system, gp_Ax3)
        self.assertAlmostSameCoord(coord_system.Location(), center)
        self.assertAlmostSameDir(coord_system.Direction(), direction)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection)

        coord_system_ = gp_Ax2(gp_Pnt(*center), gp_Dir(*direction), gp_Dir(*xdirection))
        self.assertIsInstance(coord_system_, gp_Ax2)
        coord_system = CreateUnsignedCoordSystem.as_coord_system(coord_system_)
        self.assertIsInstance(coord_system, gp_Ax3)
        self.assertAlmostSameCoord(coord_system.Location(), center)
        self.assertAlmostSameDir(coord_system.Direction(), direction)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection)

        coord_system_ = gp_Ax3(gp_Pnt(*center), gp_Dir(*direction), gp_Dir(*xdirection))
        self.assertIsInstance(coord_system_, gp_Ax3)
        coord_system = CreateUnsignedCoordSystem.as_coord_system(coord_system_)
        self.assertIsInstance(coord_system, gp_Ax3)
        self.assertAlmostSameCoord(coord_system.Location(), center)
        self.assertAlmostSameDir(coord_system.Direction(), direction)
        self.assertAlmostSameDir(coord_system.XDirection(), xdirection)

        with self.assertRaises(TypeError):
            CreateUnsignedCoordSystem.as_coord_system((0., 0.))

    def test_base_coordinate_systems(self):
        ox = CreateUnsignedCoordSystem.ox()
        self.assertIsInstance(ox, gp_Ax3)
        self.assertAlmostSameCoord(ox.Location(), (0., 0., 0.))
        self.assertAlmostSameDir(ox.Direction(), Ox)

        oy = CreateUnsignedCoordSystem.oy()
        self.assertIsInstance(oy, gp_Ax3)
        self.assertAlmostSameCoord(oy.Location(), (0., 0., 0.))
        self.assertAlmostSameDir(oy.Direction(), Oy)

        oz = CreateUnsignedCoordSystem.oz()
        self.assertIsInstance(oz, gp_Ax3)
        self.assertAlmostSameCoord(oz.Location(), (0., 0., 0.))
        self.assertAlmostSameDir(oz.Direction(), Oz)

    def test_from_location_and_directions(self):
        p = CreatePoint.as_point((10, 20, 30))
        coord_system = CreateUnsignedCoordSystem.from_location_and_directions(p, [0, 1, 0], [1, 0, 0])
        self.assertIsInstance(coord_system, gp_Ax3)
        self.assertAlmostSameCoord(coord_system.Location(), p)
        self.assertAlmostSameDir(coord_system.Direction(), Ox)
        self.assertAlmostSameDir(coord_system.XDirection(), Oy)
        self.assertAlmostSameDir(coord_system.YDirection(), Oz)
