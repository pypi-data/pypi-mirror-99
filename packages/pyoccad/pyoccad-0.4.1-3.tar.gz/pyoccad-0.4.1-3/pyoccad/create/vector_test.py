import numpy as np
from OCC.Core.gp import gp_Dir, gp_Pnt, gp_Vec, gp_XYZ, gp_Vec2d, gp_Pnt2d, gp_Dir2d, gp_XY

from pyoccad.create.vector import CreateVector
from pyoccad.tests.testcase import TestCase, tol

Ox = gp_Dir(1, 0, 0)
Oy = gp_Dir(0, 1, 0)
Oz = gp_Dir(0, 0, 1)


class CreateVectorTest(TestCase):

    def test_unit_vectors(self):
        self.assertAlmostSameCoord(CreateVector.x_vec(), gp_Vec(1, 0, 0))
        self.assertAlmostSameCoord(CreateVector.y_vec(), gp_Vec(0, 1, 0))
        self.assertAlmostSameCoord(CreateVector.z_vec(), gp_Vec(0, 0, 1))

        self.assertAlmostSameCoord(CreateVector.ox(), gp_Vec(1, 0, 0))
        self.assertAlmostSameCoord(CreateVector.oy(), gp_Vec(0, 1, 0))
        self.assertAlmostSameCoord(CreateVector.oz(), gp_Vec(0, 0, 1))

    def __test_constructor(self, f, v_2d, v_3d):
        x = (1, 2, 3)
        self.assertAlmostSameCoord(v_3d, f(gp_Pnt(*x)))
        self.assertAlmostSameCoord(v_3d, f((gp_Pnt(1, 1, 1), gp_Pnt(2, 3, 4))))
        self.assertAlmostSameCoord(v_3d, f(gp_XYZ(*x)))
        self.assertAlmostSameCoord(v_3d, f(gp_Vec(*x)))
        self.assertAlmostSameCoord(v_3d, f((gp_Dir(*x), np.linalg.norm(x))))
        self.assertAlmostSameCoord(v_3d, f(list(x)))
        self.assertAlmostSameCoord(v_3d, f(np.array(x)))

        x = (1, 2)
        self.assertAlmostSameCoord(v_2d, f(gp_Pnt2d(*x)))
        self.assertAlmostSameCoord(v_2d, f((gp_Pnt2d(), gp_Pnt2d(*x))))
        self.assertAlmostSameCoord(v_2d, f((gp_Pnt2d(1, 1), gp_Pnt2d(2, 3))))
        self.assertAlmostSameCoord(v_2d, f(gp_XY(*x)))
        self.assertAlmostSameCoord(v_2d, f(gp_Vec2d(*x)))
        self.assertAlmostSameCoord(v_2d, f((gp_Dir2d(*x), np.linalg.norm(x))))
        self.assertAlmostSameCoord(v_2d, f(list(x)))
        self.assertAlmostSameCoord(v_2d, f(np.array(x)))

        # Tuple of point(s)
        with self.assertRaises(TypeError):
            f((gp_XY(2, 3),))

        # Inconsistent dimensions
        with self.assertRaises(TypeError):
            f((gp_Pnt2d(2, 3), gp_Pnt()))

        # Wrong lengths
        with self.assertRaises(TypeError):
            f((1,))
        with self.assertRaises(TypeError):
            f((1, 2, 3, 4))

        # Wrong types
        with self.assertRaises(TypeError):
            f('a')
        with self.assertRaises(TypeError):
            f(('aa', 'aa'))
        with self.assertRaises(TypeError):
            f(('a', 'b', 'c'))
        with self.assertRaises(TypeError):
            f((1, 'b', 'c'))
        with self.assertRaises(TypeError):
            f((gp_Pnt(1, 1, 1), 'a'))

    def test_as_vector(self):
        v_2d = gp_Vec2d(1, 2)
        v_3d = gp_Vec(1, 2, 3)
        self.__test_constructor(CreateVector.as_vector, v_2d, v_3d)

    def test_as_list(self):
        v_2d = [1, 2]
        v_3d = [1, 2, 3]
        self.__test_constructor(CreateVector.as_list, v_2d, v_3d)

    def test_as_tuple(self):
        v_2d = (1, 2)
        v_3d = (1, 2, 3)
        self.__test_constructor(CreateVector.as_tuple, v_2d, v_3d)

    def test_as_ndarray(self):
        v_2d = np.r_[1, 2]
        v_3d = np.r_[1, 2, 3]
        self.__test_constructor(CreateVector.as_ndarray, v_2d, v_3d)

    def test_from_point(self):
        v_2d = gp_Vec2d(1, 2)
        v_3d = gp_Vec(1, 2, 3)
        x = (1, 2, 3)
        v = CreateVector.from_point(x)
        self.assertAlmostEqual((v_3d - v).Magnitude(), 0., delta=tol)

        x = [1, 2, 3]
        v = CreateVector.from_point(x)
        self.assertAlmostEqual((v_3d - v).Magnitude(), 0., delta=tol)

        x = (1, 2)
        v = CreateVector.from_point(x)
        self.assertAlmostEqual((v_2d - v).Magnitude(), 0., delta=tol)

        x = [1, 2]
        v = CreateVector.from_point(x)
        self.assertAlmostEqual((v_2d - v).Magnitude(), 0., delta=tol)

        x = np.r_[1, 2]
        v = CreateVector.from_point(x)
        self.assertAlmostEqual((v_2d - v).Magnitude(), 0., delta=tol)

        with self.assertRaises(TypeError):
            CreateVector.from_point([1])

        with self.assertRaises(TypeError):
            CreateVector.from_point('ab')

        with self.assertRaises(TypeError):
            CreateVector.from_point('b')

        with self.assertRaises(TypeError):
            CreateVector.from_point(np.r_[0])

    def test_from_2_points(self):
        v_3d = gp_Vec(1, 2, 3)
        start = (1, 0, 0)
        end = (2, 2, 3)
        v = CreateVector.from_2_points(start, end)
        self.assertAlmostEqual((v_3d - v).Magnitude(), 0., delta=tol)

        with self.assertRaises(Exception):
            CreateVector.from_2_points([1], [2])
        with self.assertRaises(Exception):
            CreateVector.from_2_points([1, 2], [2, 3, 4])

    def test_from_direction_norm(self):
        v_2d = gp_Vec2d(1.5 / np.sqrt(2), 1.5 / np.sqrt(2))
        v = CreateVector.from_direction_norm((2., 2.), 1.5)
        self.assertAlmostEqual((v_2d - v).Magnitude(), 0., delta=tol)
        self.assertIsInstance(v, gp_Vec2d)

        v_3d = gp_Vec(1.5 / np.sqrt(3), 1.5 / np.sqrt(3), 1.5 / np.sqrt(3))
        v = CreateVector.from_direction_norm((2., 2., 2.), 1.5)
        self.assertAlmostEqual((v_3d - v).Magnitude(), 0., delta=tol)
        self.assertIsInstance(v, gp_Vec)

    def test_from_direction_relative_tension(self):
        v_2d = gp_Vec2d(7.5 / np.sqrt(2), 7.5 / np.sqrt(2))
        v = CreateVector.from_direction_relative_tension((2., 2.), 1.5, 5)
        self.assertAlmostSameCoord(v_2d, v)
        self.assertIsInstance(v, gp_Vec2d)

        v_3d = gp_Vec(10 / np.sqrt(3), 10 / np.sqrt(3), 10. / np.sqrt(3))
        v = CreateVector.from_direction_relative_tension((5., 5., 5.), 1., 10.)
        self.assertAlmostSameCoord(v_3d, v)
        self.assertIsInstance(v, gp_Vec)
