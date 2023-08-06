from typing import Union

from OCC.Core.Adaptor2d import Adaptor2d_Curve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_Surface, Adaptor3d_HSurface
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Face

from pyoccad.typing import PointT

Curve = Union[Geom_Curve, Geom2d_Curve, TopoDS_Edge, TopoDS_Wire, Adaptor3d_Curve, Adaptor2d_Curve2d]


class CreateIntersection:
    """Factory to create intersections."""

    @staticmethod
    def between_2_curves(curve1: Curve, curve2: Curve, tol: float = 1e-10) -> PointT:
        """Compute an intersection between 2 curves.

        Parameters
        ----------
        curve1: CurveT
            First curve
        curve2: CurveT
            Second curve
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        intersection_point: PointT
            The intersection point
        """
        from pyoccad.measure import MeasureExtrema

        _, _, point1, point2 = MeasureExtrema.between_2_curves(curve1, curve2, True, tol)

        min_distance = point1.Distance(point2)
        if min_distance > tol:
            raise ArithmeticError("No intersection found between curve and surface.")

        return point1

    @staticmethod
    def between_point_and_curve(point: PointT, curve: Curve, tol: float = 1e-10) -> PointT:
        """Compute the intersection between a point and a curve.

        Parameters
        ----------
        point: PointT
            The point
        curve: CurveT
            The curve
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        point : PointT
            The point if the point is on the curve
        """
        from pyoccad.measure import MeasureExtrema

        _, curve_point = MeasureExtrema.between_point_and_curve(point, curve, True, tol)
        min_distance = point.Distance(curve_point)

        if min_distance > tol:
            raise ArithmeticError("No intersection found between curve and surface.")

        return point

    @staticmethod
    def between_point_and_surface(point: PointT,
                                  surface: Adaptor3d_Surface,
                                  tol: float = 1e-10) -> PointT:
        """Compute the intersection between a point and a surface.

        Parameters
        ----------
        point: PointT
            point
        surface: Adaptator_surface
            The surface
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        intersection_point: PointT
            The point if the point is on the surface
        """
        from pyoccad.measure import MeasureExtrema

        _, _, surface_point = MeasureExtrema.between_point_and_surface(point, surface, True, tol)
        min_distance = point.Distance(surface_point)

        if min_distance > tol:
            raise ArithmeticError("No intersection found between curve and surface.")

        return point

    @staticmethod
    def between_curve_and_surface(curve: Curve,
                                  surface: Union[Geom_Surface, TopoDS_Face, Adaptor3d_Surface, Adaptor3d_HSurface],
                                  tol: float = 1e-10) -> PointT:
        """Compute the intersection between a curve and a surface.

        Parameters
        ----------
        curve: CurveT
            The curve
        surface: Union[Geom_Surface, TopoDS_Face, Adaptor3d_Surface, Adaptor3d_HSurface]
            The surface
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        intersection_point: PointT
           The intersection point
        """

        from pyoccad.measure import MeasureExtrema

        curve_point, surface_point = MeasureExtrema.between_curve_and_surface(curve, surface, True, tol)[3:]
        min_distance = curve_point.Distance(surface_point)

        if min_distance > tol:
            raise ArithmeticError("No intersection found between curve and surface.")

        return curve_point
