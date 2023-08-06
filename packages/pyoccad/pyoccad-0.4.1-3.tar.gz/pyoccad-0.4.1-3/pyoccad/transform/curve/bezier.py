from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.Geom2d import Geom2d_BezierCurve
from OCC.Core.GeomAPI import geomapi
from OCC.Core.gp import gp_Pln


class TransformBezier:
    """Factory to transform Bezier curves."""

    @staticmethod
    def to_3d(bezier: Geom2d_BezierCurve, plane: gp_Pln = gp_Pln()) -> Geom_BezierCurve:
        """Create a 3D bezier curve from a 2D Bezier curve

        Parameters
        ----------
        bezier : Geom2d_BezierCurve
            The 2D Bezier curve
        plane : gp_Pln, optional
            The plane where the 2D bezier curve shall be positioned

        Returns
        -------
        bezier_curve : Geom_BezierCurve
            the Bezier curve in the plane
        """
        return Geom_BezierCurve.DownCast(geomapi.To3d(bezier, plane))

    @staticmethod
    def to_2d(bezier: Geom_BezierCurve, plane: gp_Pln = gp_Pln()) -> Geom2d_BezierCurve:
        """Create a 2D bezier curve from a 3D Bezier curve

        Parameters
        ----------
        bezier : Geom_BezierCurve
            The 3D Bezier curve
        plane : gp_Pln, optional
            The plane where the projection is made

        Returns
        -------
        bezier_curve : Geom2d_BezierCurve
            The 2D projected Bezier curve on the plane
        """
        return Geom2d_BezierCurve.DownCast(geomapi.To2d(bezier, plane))
