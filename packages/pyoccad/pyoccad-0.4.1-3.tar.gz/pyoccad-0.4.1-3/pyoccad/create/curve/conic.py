from math import sin, cos, atan, pi, sqrt
from typing import Tuple

from OCC.Core.Geom import Geom_TrimmedCurve, Geom_Ellipse
from OCC.Core.Geom2d import Geom2d_Ellipse, Geom2d_TrimmedCurve
from OCC.Core.Precision import precision
from OCC.Core.ProjLib import projlib
from OCC.Core.gp import gp_Pln, gp_Ax3, gp_Lin, gp_Pnt2d, gp_Dir2d, gp_Ax22d, gp_Ax2d, gp_Ax1
from scipy.optimize import root

from pyoccad.create import CreateCurve


class CreateConic:
    """Factory to create conic curves."""

    @staticmethod
    def __find_bi_tangent_2d_ellipse(axis1: gp_Ax2d, axis2: gp_Ax2d,
                                     e: float) -> Tuple[Geom2d_Ellipse, float, float]:
        """Build one of the bi-tangent elliptic arc.

        Parameters
        ----------
        axis1: gp_Ax2d
            First tangent axis
        axis2: gp_Ax2d
            Second tangent axis
        e: float
            Ellipse excentricity

        Returns
        -------
        ellipse, theta1, theta2: Tuple[Geom2d_Ellipse, float, float]
            The ellipse and positions of the two axes on it
        """

        def equation(x, *p):
            e, ax1, ax2 = p

            x1 = ax1.Location().X()
            x2 = ax2.Location().X()
            y1 = ax1.Location().Y()
            y2 = ax2.Location().Y()

            t1x = ax1.Direction().X()
            t2x = ax2.Direction().X()
            t1y = ax1.Direction().Y()
            t2y = ax2.Direction().Y()

            theta1 = x[0]
            theta2 = x[1]
            theta0 = atan(
                ((y1 - y2) * cos(theta1) + (-y1 + y2) * cos(theta2) - e * (x1 - x2) * (sin(theta1) - sin(theta2))) /
                ((x1 - x2) * cos(theta1) + (-x1 + x2) * cos(theta2) + e * (y1 - y2) * (sin(theta1) - sin(theta2))))

            a = -(cos(theta0) * x1 - cos(theta0) * x2 + sin(theta0) *
                  y1 - sin(theta0) * y2) / (cos(theta2) - cos(theta1))
            if a <= 0:
                a = -a
                theta0 = theta0 + pi
                # t = theta1
                # theta1 = theta2
                # theta2 = t

            f = [-e * (t1x * sin(theta0) - t1y * cos(theta0)) * cos(theta1) -
                 (cos(theta0) * t1x + sin(theta0) * t1y) * sin(theta1) - sqrt(1 + (e ** 2 - 1) * cos(theta1) ** 2),
                 -e * (t2x * sin(theta0) - t2y * cos(theta0)) * cos(theta2) -
                 (cos(theta0) * t2x + sin(theta0) * t2y) * sin(theta2) - sqrt(1 + (e ** 2 - 1) * cos(theta2) ** 2)]
            return f

        # Init solution
        theta1 = 0.
        theta2 = pi
        xi = [theta1, theta2]
        # params
        p = (e, axis1, axis2)
        # Minimize
        sol = root(equation, xi, args=p, options={'maxfev': 8000, })
        # sol = root(eq, xi, args=p, method='lm',options={'maxfev': 8000})
        x = sol.x
        # x = fsolve(eq, xi ,args=p)
        # Construction
        theta1 = x[0]
        theta2 = x[1]
        x1 = axis1.Location().X()
        x2 = axis2.Location().X()
        y1 = axis1.Location().Y()
        y2 = axis2.Location().Y()

        theta0 = atan(
            ((y1 - y2) * cos(theta1) + (-y1 + y2) * cos(theta2) - e * (x1 - x2) * (sin(theta1) - sin(theta2))) /
            ((x1 - x2) * cos(theta1) + (-x1 + x2) * cos(theta2) + e * (y1 - y2) * (sin(theta1) - sin(theta2))))

        a = -(cos(theta0) * x1 - cos(theta0) * x2 + sin(theta0) *
              y1 - sin(theta0) * y2) / (cos(theta2) - cos(theta1))

        if a <= 0:
            a = -a
            theta0 = theta0 + pi
            # t = theta1
            # theta1 = theta2
            # theta2 = t

        x0 = x1 - (cos(theta0) * a * cos(theta1) - sin(theta0) * a * e * sin(theta1))
        y0 = y1 - (sin(theta0) * a * cos(theta1) + cos(theta0) * a * e * sin(theta1))

        x_dir_ax = gp_Dir2d(cos(theta0), sin(theta0))
        ell = Geom2d_Ellipse(gp_Ax22d(gp_Pnt2d(x0, y0), x_dir_ax), a, a * e)

        return ell, theta1, theta2

    @staticmethod
    def bi_tangent_2d_ellipse(axis1: gp_Ax2d, axis2: gp_Ax2d, e: float) -> Geom2d_Ellipse:
        """Build a bi-tangent ellipse.

        Parameters
        ----------
        axis1: gp_Ax2d
            First tangent axis
        axis2: gp_Ax2d
            Second tangent axis
        e: float
            Ellipse excentricity

        Returns
        -------
        ellipse: Geom2d_Ellipse
            The resulting ellipse
        """
        return CreateConic.__find_bi_tangent_2d_ellipse(axis1, axis2, e)[0]

    @staticmethod
    def bi_tangent_2d_ellipse_arc(axis1: gp_Ax2d, axis2: gp_Ax2d, e: float) -> Geom2d_TrimmedCurve:
        """Build a bi-tangent elliptic arc.

        Parameters
        ----------
        axis1: gp_Ax2d
            First tangent axis
        axis2: gp_Ax2d
            Second tangent axis
        e: float
            Ellipse excentricity

        Returns
        -------
        trimmed_ellipse : Geom2d_TrimmedCurve
            The resulting trimmed ellipse
        """
        return Geom2d_TrimmedCurve(*CreateConic.__find_bi_tangent_2d_ellipse(axis1, axis2, e))

    @staticmethod
    def __find_bi_tangent_ellipse(axis1: gp_Ax1, axis2: gp_Ax1,
                                  e: float, tol=precision.Confusion()) -> Tuple[Geom2d_Ellipse, float, float]:
        """Build one of the bi-tangent elliptic arc.

        Parameters
        ----------
        axis1: gp_Ax1
            First tangent axis
        axis2: gp_Ax1
            Second tangent axis
        e: float
            Ellipse excentricity
        tol: float
            Tolerance for algorithm

        Returns
        -------
        ellipse, theta1, theta2: Tuple[Geom2d_Ellipse, float, float]
            The ellipse and positions of the two axes on it
        """
        from pyoccad.transform import Move

        direction = axis1.Direction().Crossed(axis2.Direction())
        pln = gp_Pln(gp_Ax3(axis1.Location(), direction, axis1.Direction()))

        if pln.Distance(axis2.Location()) > tol:
            raise ValueError('Tangent directions not compatible with points location')

        # axis projection method does not exist, use a trick
        ax1_2d = projlib.Project(pln, gp_Lin(axis1)).Position()
        ax2_2d = projlib.Project(pln, gp_Lin(axis2)).Position()
        ellipse, theta1, theta2 = CreateConic.__find_bi_tangent_2d_ellipse(ax1_2d, ax2_2d, e)
        return CreateCurve.from_2d(ellipse, pln), theta1, theta2

    @staticmethod
    def bi_tangent_ellipse(axis1: gp_Ax1, axis2: gp_Ax1, e: float, tol=precision.Confusion()) -> Geom_Ellipse:
        """Build one of the bi-tangent elliptic arc.

        Parameters
        ----------
        axis1: gp_Ax1
            First tangent axis
        axis2: gp_Ax1
            Second tangent axis
        e: float
            Ellipse excentricity
        tol: float
            Tolerance for algorithm

        Returns
        -------
        ellipse : Geom_Ellipse
            The resulting ellipse
        """
        return CreateConic.__find_bi_tangent_ellipse(axis1, axis2, e, tol)[0]


    @staticmethod
    def bi_tangent_ellipse_arc(axis1: gp_Ax1, axis2: gp_Ax1, e: float, tol=precision.Confusion()) -> Geom_TrimmedCurve:
        """Build one of the bi-tangent elliptic arc.

        Parameters
        ----------
        axis1: gp_Ax1
            First tangent axis
        axis2: gp_Ax1
            Second tangent axis
        e: float
            Ellipse excentricity
        tol: float
            Tolerance for algorithm

        Returns
        -------
        trimmed_ellipse : Geom_TrimedCurve
            The resulting trimmed ellipse
        """
        return Geom_TrimmedCurve(*CreateConic.__find_bi_tangent_ellipse(axis1, axis2, e, tol))
