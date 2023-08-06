from math import sqrt

from OCC.Core.gp import (gp_Pnt, gp_Pnt2d)

from pyoccad.create.curve.bezier import CreateBezier
from pyoccad.tests.testcase import TestCase, angTol
from pyoccad.transform.curve.bezier import TransformBezier


class TransformBezierTest(TestCase):

    def setUp(self):
        self.poles = [gp_Pnt(0, 0, 0),
                      [1, 0, 0],
                      gp_Pnt(1, 1, 0),
                      (2, 1, 0)]

        self.poles2d = [gp_Pnt2d(0, 0),
                        [1, 0],
                        gp_Pnt2d(1, 1),
                        (2, 1)]

    def test_to_3d(self):
        poles = [[0, 0],
                 [1, 0],
                 [1, 1],
                 [2, 1]]
        bez2d = CreateBezier.from_poles(poles)
        bez = TransformBezier.to_3d(bez2d)
        b_poles = bez.Poles()
        self.assertEqual(b_poles.Length(), len(poles))
        for i, p in enumerate(poles):
            self.assertAlmostEqual(sqrt((p[0] - b_poles.Value(i + 1).X()) ** 2 +
                                        (p[1] - b_poles.Value(i + 1).Y()) ** 2), 0., delta=angTol)

    def test_to_2d(self):
        poles = [[0, 0, 0],
                 [1, 0, 0],
                 [1, 1, 0],
                 [2, 1, 0]]
        bez = CreateBezier.from_poles(poles)
        bez2d = TransformBezier.to_2d(bez)
        b_poles = bez2d.Poles()
        self.assertEqual(b_poles.Length(), len(poles))
        for i, p in enumerate(poles):
            self.assertAlmostEqual(sqrt((p[0] - b_poles.Value(i + 1).X()) ** 2 +
                                        (p[1] - b_poles.Value(i + 1).Y()) ** 2), 0., delta=angTol)
