import numpy as np
from OCC.Core.gp import gp_Dir, gp_Vec, gp_Vec2d

from pyoccad.measure.vector import MeasureVector
from pyoccad.tests.testcase import TestCase

Ox = gp_Dir(1, 0, 0)
Oy = gp_Dir(0, 1, 0)
Oz = gp_Dir(0, 0, 1)


class MeasureVectorTest(TestCase):

    def test_dimension(self):
        v_2d = gp_Vec2d(1, 2)
        v_3d = gp_Vec(1, 2, 3)
        v_tuple = (1., 2., 30.)
        v_list = [0., 2.]
        v_np = np.r_[10., 2., 53.]

        self.assertEqual(2, MeasureVector.dimension(v_2d))
        self.assertEqual(3, MeasureVector.dimension(v_3d))
        self.assertEqual(3, MeasureVector.dimension(v_tuple))
        self.assertEqual(2, MeasureVector.dimension(v_list))
        self.assertEqual(3, MeasureVector.dimension(v_np))
