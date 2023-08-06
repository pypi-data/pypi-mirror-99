import numpy as np
from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Pnt2d, gp_XY

from pyoccad.measure import MeasurePoint
from pyoccad.tests.testcase import TestCase


class MeasurePointTest(TestCase):

    def test_dimension(self):
        self.assertEqual(2., MeasurePoint.dimension(gp_Pnt2d(1, 2)))
        self.assertEqual(3., MeasurePoint.dimension(gp_Pnt(1, 2, 3)))
        self.assertEqual(2., MeasurePoint.dimension(gp_XY(1, 2)))
        self.assertEqual(3., MeasurePoint.dimension(gp_XYZ(1, 2, 3)))
        self.assertEqual(2., MeasurePoint.dimension((1, 2)))
        self.assertEqual(3., MeasurePoint.dimension((1, 2, 3)))
        self.assertEqual(2., MeasurePoint.dimension([1, 2]))
        self.assertEqual(3., MeasurePoint.dimension([1, 2, 3]))
        self.assertEqual(2., MeasurePoint.dimension(np.r_[1, 2]))
        self.assertEqual(3., MeasurePoint.dimension(np.r_[1, 2, 3]))

        with self.assertRaises(TypeError):
            MeasurePoint.dimension((1, 2, 3, 4))
        with self.assertRaises(TypeError):
            MeasurePoint.dimension((1, ))
        with self.assertRaises(TypeError):
            MeasurePoint.dimension([1., 2., 3., 4.])
        with self.assertRaises(TypeError):
            MeasurePoint.dimension([1.])
        with self.assertRaises(TypeError):
            MeasurePoint.dimension(np.r_[1., 2., 3., 4.])
        with self.assertRaises(TypeError):
            MeasurePoint.dimension(np.r_[1.])

    def test_check_dimension_equals(self):
        self.assertEqual(3, MeasurePoint.unique_dimension([gp_Pnt(), gp_Pnt()]))
        self.assertEqual(2, MeasurePoint.unique_dimension([gp_Pnt2d(), gp_Pnt2d()]))

        with self.assertRaises(TypeError):
            MeasurePoint.unique_dimension([gp_Pnt(), gp_Pnt2d()])
