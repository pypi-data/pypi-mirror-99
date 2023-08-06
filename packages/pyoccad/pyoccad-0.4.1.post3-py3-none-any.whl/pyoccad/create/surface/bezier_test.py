from OCC.Core.Geom import Geom_BezierCurve

from pyoccad.create.curve.bezier import CreateBezier
from pyoccad.create.surface.bezier import CreateBezierSurface
from pyoccad.tests.testcase import TestCase


class CreateBezierSurfaceTest(TestCase):

    def test_from_poles(self):
        p = list()
        p.append([[0, 0, 0], [1, 2, 0], [3, 4, 0]])
        p.append([[0, 0, 1], [1, 2, 1], [3, 4, 1]])

        bez_surf = CreateBezierSurface.from_poles(p)
        bez_curv = CreateBezier.from_poles(p[0])
        u_iso = Geom_BezierCurve.DownCast(bez_surf.UIso(0.))
        n1 = u_iso.NbPoles()
        n2 = bez_curv.NbPoles()
        self.assertEqual(n1, n2)
        for i in range(n1):
            self.assertAlmostSameCoord(u_iso.Pole(i + 1), bez_curv.Pole(i + 1))

        w = [[1, 1, 2],
             [2, 1, 2]]
        bez_surf = CreateBezierSurface.from_poles_and_weights(p, w)
        for i, pi in enumerate(p):
            for j, pij in enumerate(pi):
                self.assertAlmostSameCoord(bez_surf.Pole(i + 1, j + 1), pij)
