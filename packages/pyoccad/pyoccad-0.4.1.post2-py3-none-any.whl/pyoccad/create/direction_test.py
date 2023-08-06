from math import degrees

import numpy as np
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_XYZ, gp_Dir2d, gp_Pnt2d, gp_Vec2d, gp_XY

from pyoccad.create.direction import CreateDirection
from pyoccad.tests.testcase import TestCase


class TestDir(TestCase):

    def setUp(self):
        self.slope = np.pi / 3
        self.slope_deg = degrees(self.slope)

    def __test_constructor(self, f, dir_2d, dir_3d):
        # OCC types
        self.assertAlmostSameDir(dir_2d, f(gp_Dir2d(1, 2)))
        self.assertAlmostSameDir(dir_3d, f(gp_Dir(1, 2, 3)))
        self.assertAlmostSameDir(dir_2d, f(gp_XY(1, 2)))
        self.assertAlmostSameDir(dir_3d, f(gp_XYZ(1, 2, 3)))
        self.assertAlmostSameDir(dir_2d, f(gp_Pnt2d(1, 2)))
        self.assertAlmostSameDir(dir_3d, f(gp_Pnt(1, 2, 3)))
        self.assertAlmostSameDir(dir_2d, f(gp_Vec2d(1, 2)))
        self.assertAlmostSameDir(dir_3d, f(gp_Vec(1, 2, 3)))
        # Python types
        self.assertAlmostSameDir(dir_2d, f((1, 2)))
        self.assertAlmostSameDir(dir_3d, f((1, 2, 3)))
        self.assertAlmostSameDir(dir_2d, f([1, 2]))
        self.assertAlmostSameDir(dir_3d, f([1, 2, 3]))
        # Numpy types
        self.assertAlmostSameDir(dir_2d, f(np.r_[1, 2]))
        self.assertAlmostSameDir(dir_3d, f(np.r_[1, 2, 3]))
        # Mixing Python types
        self.assertAlmostSameDir(dir_2d, f((1., 2)))
        self.assertAlmostSameDir(dir_3d, f((10, 20., 30)))

        # Tuple of point(s)
        with self.assertRaises(TypeError):
            f((gp_XY(2, 3),))

        # Wrong lengths
        with self.assertRaises(TypeError):
            f((1,))
        with self.assertRaises(TypeError):
            f((1, 2, 3, 4))
        with self.assertRaises(TypeError):
            f(np.r_[1, 2, 3, 4])

        # Wrong types
        with self.assertRaises(TypeError):
            f('a')
        with self.assertRaises(TypeError):
            f(('aa', 'aa'))
        with self.assertRaises(TypeError):
            f(('a', 'b', 'c'))
        with self.assertRaises(TypeError):
            f((1, 'b', 'c'))

    def test_as_direction(self):
        dir_2d = gp_Dir2d(1, 2)
        dir_3d = gp_Dir(1, 2, 3)
        self.__test_constructor(CreateDirection.as_direction, dir_2d, dir_3d)
    
    def test_as_list(self):
        dir_2d = [1, 2]
        dir_3d = [1, 2, 3]
        self.__test_constructor(CreateDirection.as_list, dir_2d, dir_3d)

    def test_as_tuple(self):
        dir_2d = (1, 2)
        dir_3d = (1, 2, 3)
        self.__test_constructor(CreateDirection.as_tuple, dir_2d, dir_3d)

    def test_as_ndarray(self):
        dir_2d = np.r_[1, 2]
        dir_3d = np.r_[1, 2, 3]
        self.__test_constructor(CreateDirection.as_ndarray, dir_2d, dir_3d)

    def test_x_dir(self):
        self.assertAlmostSameDir(CreateDirection.x_dir(), gp_Dir(1, 0, 0))
        self.assertAlmostSameDir(CreateDirection.ox(), gp_Dir(1, 0, 0))

    def test_y_dir(self):
        self.assertAlmostSameDir(CreateDirection.y_dir(), gp_Dir(0, 1, 0))
        self.assertAlmostSameDir(CreateDirection.oy(), gp_Dir(0, 1, 0))

    def test_z_dir(self):
        self.assertAlmostSameDir(CreateDirection.z_dir(), gp_Dir(0, 0, 1))
        self.assertAlmostSameDir(CreateDirection.oz(), gp_Dir(0, 0, 1))

    def test_in_xy_plane(self):
        slope, slope_deg = self.slope, self.slope_deg
        ref_dir = gp_Dir(0.5, np.sqrt(3) / 2., 0)
        self.assertAlmostSameDir(CreateDirection.in_xy_plane(slope), ref_dir)
        self.assertAlmostSameDir(CreateDirection.in_xy_plane_deg(slope_deg), ref_dir)

    def test_in_xz_plane(self):
        slope, slope_deg = self.slope, self.slope_deg
        ref_dir = gp_Dir(0.5, 0., -np.sqrt(3) / 2)
        self.assertAlmostSameDir(CreateDirection.in_xz_plane(slope), ref_dir)
        self.assertAlmostSameDir(CreateDirection.in_xz_plane_deg(slope_deg), ref_dir)

    def test_in_zx_plane(self):
        slope, slope_deg = self.slope, self.slope_deg
        ref_dir = gp_Dir(np.sqrt(3) / 2, 0., 0.5)
        self.assertAlmostSameDir(CreateDirection.in_zx_plane(slope), ref_dir)
        self.assertAlmostSameDir(CreateDirection.in_zx_plane_deg(slope_deg), ref_dir)

    def test_in_zy_plane(self):
        slope, slope_deg = self.slope, self.slope_deg
        ref_dir = gp_Dir(0., -np.sqrt(3) / 2., 0.5)
        self.assertAlmostSameDir(CreateDirection.in_zy_plane(slope), ref_dir)
        self.assertAlmostSameDir(CreateDirection.in_zy_plane_deg(slope_deg), ref_dir)
