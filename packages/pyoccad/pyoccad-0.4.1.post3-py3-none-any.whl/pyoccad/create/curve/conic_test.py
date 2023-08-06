from math import pi, sin, cos, radians

from OCC.Core.gp import (gp_Pnt, gp_Dir, gp_Ax1)

from pyoccad.create.curve.conic import CreateConic
from pyoccad.tests.testcase import TestCase


class CreateConicTest(TestCase):

    def test_bi_tangent_ellipse(self):
        e = 0.2
        a1 = pi
        a2 = radians(180 + 95)

        x1 = -661.621
        y1 = 1358.424
        x2 = -2083.973
        y2 = 1071.813

        ax1 = gp_Ax1(gp_Pnt(x1, 0, y1), gp_Dir(cos(a1), 0, sin(a1)))
        ax2 = gp_Ax1(gp_Pnt(x2, 0, y2), gp_Dir(cos(a2), 0, sin(a2)))

        arc = CreateConic.bi_tangent_ellipse_arc(ax1, ax2, e)

        u1 = arc.FirstParameter()
        u2 = arc.LastParameter()

        self.assertAlmostSameCoord(ax1.Location(), arc.Value(u1))
        self.assertAlmostSameCoord(ax2.Location(), arc.Value(u2))

        # l1 = trim.curve(line.from_point_and_dir(ax1.Location(), ax1.Direction()), 0, 30.)
        # l2 = trim.curve(line.from_point_and_dir(ax2.Location(), ax2.Direction()), 0, 30.)
        # ell = Geom_Ellipse.DownCast(Geom_TrimmedCurve.DownCast(arc).BasisCurve())
        #
        # center = ell.Elips().XAxis().Location()
        # radius = ell.Elips().MajorRadius()
        # lx = trim.curve(line.from_ax1(ell.Elips().XAxis()), 0, radius / 10)
        # ly = trim.curve(line.from_ax1(ell.Elips().YAxis()), 0, radius / 10)
