import unittest

from OCC.Core.gp import gp_Dir, gp_Dir2d

tol = 1e-6
angTol = 1e-4


class TestCase(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.tol = 1e-6
        self.angTol = 1e-4

    def set_tol(self, tol):
        self.tol = tol

    def assertAlmostSameCoord(self, x1, x2):
        from pyoccad.create.point import CreatePoint
        from pyoccad.measure import MeasurePoint

        point1 = CreatePoint.as_point(x1)
        point2 = CreatePoint.as_point(x2)
        dimension = MeasurePoint.unique_dimension((point1, point2))

        if dimension == 3:
            self.assertAlmostEqual((point1.XYZ() - point2.XYZ()).Modulus(), 0., delta=tol)
        elif dimension == 2:
            self.assertAlmostEqual((point1.XY() - point2.XY()).Modulus(), 0., delta=tol)

    def assertAlmostSameDir(self, x1, x2):
        from pyoccad.create.direction import CreateDirection

        d1 = CreateDirection.as_direction(x1)
        d2 = CreateDirection.as_direction(x2)
        self.assertTrue(d1.IsEqual(d2, angTol))

    def assertAlmostParallel(self, x1, x2):
        from pyoccad.create.point import CreatePoint

        try:
            d1 = gp_Dir(CreatePoint.as_point(x1).XYZ())
            d2 = gp_Dir(CreatePoint.as_point(x2).XYZ())
        except:
            try:
                d1 = gp_Dir2d(CreatePoint.as_point(x1).XY())
                d2 = gp_Dir2d(CreatePoint.as_point(x2).XY())
            except:
                raise Exception
        self.assertTrue(d1.IsParallel(d2, angTol))

    def assertAlmostEqualValues(self, v1, v2):
        super().assertAlmostEqual(v1, v2, delta=self.tol)

    def assertAlmostNullValue(self, v):
        super().assertAlmostEqual(v, 0., delta=self.tol)

    def assertAlmostEqualAngles(self, v1, v2):
        super().assertAlmostEqual(v1, v2, delta=self.angTol)

    def assertAlmostNullAngle(self, v):
        super().assertAlmostEqual(v, 0., delta=self.angTol)
