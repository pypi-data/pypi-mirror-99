from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec

from pyoccad.create import CreateControlPoint, CreateVector
from pyoccad.tests.testcase import TestCase, tol


class ControlPointTest(TestCase):

    def test_control_point(self):
        cp = CreateControlPoint.from_point((1., 2., 3.))
        self.assertAlmostEqual(cp.Distance(gp_Pnt(1, 2, 3)), 0., delta=tol)
        self.assertFalse(cp.has_d1)

        cp.d1 = CreateVector.from_point([5, 0, 0])
        self.assertTrue(cp.has_d1)
        self.assertTrue(cp.d1_dir.IsEqual(gp_Dir(1, 0, 0), tol))
        self.assertTrue(cp.d1.IsEqual(gp_Vec(5, 0, 0), tol, tol))

        cp.d2 = [0, 2.2, 0]
        self.assertTrue(cp.has_d1)
        self.assertTrue(cp.d2_dir.IsEqual(gp_Dir(0, 1, 0), tol))
        self.assertTrue(cp.d2.IsEqual(gp_Vec(0, 2.2, 0), tol, tol))

        cp = CreateControlPoint.from_point(gp_Pnt(0.2, 0.3, 10.))
        self.assertAlmostEqual(cp.Distance(gp_Pnt(0.2, 0.3, 10)), 0., delta=tol)

        with self.assertRaises(AttributeError):
            cp.d1 = [0, 2.2]

        with self.assertRaises(AttributeError):
            cp.d2 = [0, 2.2]
