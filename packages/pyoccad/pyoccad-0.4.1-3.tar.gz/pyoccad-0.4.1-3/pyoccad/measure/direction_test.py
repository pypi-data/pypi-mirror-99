import numpy as np
from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Pnt2d, gp_XY, gp_Dir, gp_Dir2d, gp_Vec, gp_Vec2d

from pyoccad.measure import MeasureDirection
from pyoccad.tests.testcase import TestCase


class MeasureDirectionTest(TestCase):

    def test_dimension(self):
        # OCC types
        self.assertEqual(2., MeasureDirection.dimension(gp_Dir2d(1, 2)))
        self.assertEqual(3., MeasureDirection.dimension(gp_Dir(1, 2, 3)))
        self.assertEqual(2., MeasureDirection.dimension(gp_XY(1, 2)))
        self.assertEqual(3., MeasureDirection.dimension(gp_XYZ(1, 2, 3)))
        self.assertEqual(2., MeasureDirection.dimension(gp_Pnt2d(1, 2)))
        self.assertEqual(3., MeasureDirection.dimension(gp_Pnt(1, 2, 3)))
        self.assertEqual(2., MeasureDirection.dimension(gp_Vec2d(1, 2)))
        self.assertEqual(3., MeasureDirection.dimension(gp_Vec(1, 2, 3)))
        # Python types
        self.assertEqual(2., MeasureDirection.dimension((1, 2)))
        self.assertEqual(3., MeasureDirection.dimension((1, 2, 3)))
        self.assertEqual(2., MeasureDirection.dimension([1, 2]))
        self.assertEqual(3., MeasureDirection.dimension([1, 2, 3]))
        # Numpy types
        self.assertEqual(2., MeasureDirection.dimension(np.r_[1, 2]))
        self.assertEqual(3., MeasureDirection.dimension(np.r_[2, 3, 4]))
        # Mixing types
        self.assertEqual(2., MeasureDirection.dimension((1., 2)))
        self.assertEqual(3., MeasureDirection.dimension((1, 2., np.sqrt(2))))

        # Tuple of point(s)
        with self.assertRaises(TypeError):
            MeasureDirection.dimension((gp_XY(2, 3), ))

        # Wrong lengths
        with self.assertRaises(TypeError):
            MeasureDirection.dimension((1, ))
        with self.assertRaises(TypeError):
            MeasureDirection.dimension((1, 2, 3, 4))

        # Wrong types
        with self.assertRaises(TypeError):
            MeasureDirection.dimension('a')
        with self.assertRaises(TypeError):
            MeasureDirection.dimension(('aa', 'aa'))
        with self.assertRaises(TypeError):
            MeasureDirection.dimension(('a', 'b', 'c'))
        with self.assertRaises(TypeError):
            MeasureDirection.dimension((1, 'b', 'c'))
