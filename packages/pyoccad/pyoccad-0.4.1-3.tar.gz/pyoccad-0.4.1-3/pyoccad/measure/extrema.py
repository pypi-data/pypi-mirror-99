from typing import Union, Tuple, Collection

import numpy as np
from OCC.Core.Adaptor2d import Adaptor2d_Curve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_Surface, Adaptor3d_HSurface
from OCC.Core.Extrema import Extrema_ExtCC, Extrema_POnCurv, Extrema_ExtCC2d, Extrema_POnCurv2d, Extrema_ExtPC, \
    Extrema_ExtPC2d, Extrema_ExtPS, Extrema_ExtCS, Extrema_POnSurf
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Face

from pyoccad.measure import MeasureCurve, MeasurePoint
from pyoccad.typing import PointT

Curve = Union[Geom_Curve, Geom2d_Curve, TopoDS_Edge, TopoDS_Wire, Adaptor3d_Curve, Adaptor2d_Curve2d]


class MeasureExtrema:
    """Factory to measure extrema."""

    @staticmethod
    def _get_extremum_index(extrema: Collection, use_smallest: bool) -> int:
        """Return the extremum index from a collection of extrema distances.

        Parameters
        ----------
        extrema: Collection[float]
            The collection of distances
        use_smallest: bool
            Whether to use the smallest extremum or not

        Returns
        -------
            The index of the extremum in the OpenCascade convention (first item has index 1)
        """
        if len(extrema) == 0:
            raise ArithmeticError("No extremum found.")

        if use_smallest:
            index = np.argmin(extrema)
        else:
            index = np.argmax(extrema)
        return int(index) + 1

    @staticmethod
    def between_2_curves(curve1: Curve, curve2: Curve,
                         use_smallest: bool, tol: float = 1e-10) -> Tuple[float, float, PointT, PointT]:
        """Compute an extrema between 2 curves.

        Parameters
        ----------
        curve1: CurveT
            First curve
        curve2: CurveT
            Second curve
        use_smallest: bool
            Whether the smallest extremum or not
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        u1, u2, point1, point2: Tuple[float, float, PointT, PointT]
            A tuple of the parameters on the curves and the corresponding points at the extrema
        """
        from pyoccad.create.curve.curve import CreateCurve

        adaptor1 = CreateCurve.as_adaptor(curve1)
        adaptor2 = CreateCurve.as_adaptor(curve2)
        dimension = MeasureCurve.unique_dimension((adaptor1, adaptor2))

        if dimension == 3:
            extrema_curve_curve = Extrema_ExtCC(adaptor1, adaptor2, tol, tol)
            point1 = Extrema_POnCurv()
            point2 = Extrema_POnCurv()
        else:  # dimension == 2
            extrema_curve_curve = Extrema_ExtCC2d(adaptor1, adaptor2, tol, tol)
            point1 = Extrema_POnCurv2d()
            point2 = Extrema_POnCurv2d()

        index = MeasureExtrema._get_extremum_index([extrema_curve_curve.SquareDistance(i)
                                                    for i in range(1, extrema_curve_curve.NbExt() + 1)], use_smallest)

        extrema_curve_curve.Points(index, point1, point2)
        return point1.Parameter(), point2.Parameter(), point1.Value(), point2.Value()

    @staticmethod
    def between_point_and_curve(point: PointT, curve: Curve,
                                use_smallest: bool, tol: float = 1e-10) -> Tuple[float, PointT]:
        """Compute an extrema between a point and a curve.

        Parameters
        ----------
        point: PointT
            The point
        curve: CurveT
            The curve
        use_smallest: bool
            Whether the smallest extremum or not
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        u, point : Tuple[float, PointT]
            A tuple of the curve parameter and the corresponding point at the extrema
        """
        from pyoccad.create.curve.curve import CreateCurve

        dimension = MeasureCurve.dimension(curve)
        if dimension != MeasurePoint.dimension(point):
            raise TypeError('PointT and curve dimensions should match, '
                            'got dimensions {} and {}.'.format(MeasurePoint.dimension(point),
                                                               MeasureCurve.dimension(curve)))

        curve_adaptor = CreateCurve.as_adaptor(curve)

        if dimension == 3:
            extrema_point_curve = Extrema_ExtPC(point, curve_adaptor, tol)
        else:  # dimension == 2
            extrema_point_curve = Extrema_ExtPC2d(point, curve_adaptor, tol)

        index = MeasureExtrema._get_extremum_index([extrema_point_curve.SquareDistance(i)
                                                    for i in range(1, extrema_point_curve.NbExt() + 1)], use_smallest)

        extrema_point = extrema_point_curve.Point(index)
        return extrema_point.Parameter(), extrema_point.Value()

    @staticmethod
    def between_point_and_surface(point: PointT,
                                  surface: Adaptor3d_Surface,
                                  use_smallest: bool,
                                  tol: float = 1e-10) -> Tuple[float, float, PointT]:
        """Compute an extrema between a point and a surface.

        Parameters
        ----------
        point: PointT
            point
        surface: Adaptator_surface
            The surface
        use_smallest: bool
            Whether the smallest extremum or not
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        u, v, intersection_point: Tuple[float, float, PointT]
            A tuple of the surface parameters (u, v) and the corresponding point at the extrema
        """
        from pyoccad.create import CreatePoint

        extrema_point_surface = Extrema_ExtPS(CreatePoint.as_point(point), surface, tol, tol)

        index = MeasureExtrema._get_extremum_index([extrema_point_surface.SquareDistance(i)
                                                    for i in range(1, extrema_point_surface.NbExt() + 1)], use_smallest)
        extrema_point = extrema_point_surface.Point(index)
        u, v = extrema_point.Parameter()
        return u, v, extrema_point.Value()

    @staticmethod
    def between_curve_and_surface(curve: Curve,
                                  surface: Union[Geom_Surface, TopoDS_Face, Adaptor3d_Surface, Adaptor3d_HSurface],
                                  use_smallest: bool,
                                  tol: float = 1e-10) -> Tuple[float, float, float, PointT, PointT]:
        """Compute an extrema between a curve and a surface.

        Parameters
        ----------
        curve: CurveT
            The curve
        surface: Union[Geom_Surface, TopoDS_Face, Adaptor3d_Surface, Adaptor3d_HSurface]
            The surface
        use_smallest: bool
            Whether the smallest extremum or not
        tol: float, optional
            Tolerance for the algorithm {default=1e-10}

        Returns
        -------
        u_curve, u_surface, v_surface, curve_point, surface_point: Tuple[float, float, float, PointT, PointT]
            A tuple of the curve and surface parameters and the corresponding points at the extrema
        """
        from pyoccad.create import CreateSurface, CreateCurve

        extrema_curve_surface = Extrema_ExtCS(CreateCurve.as_adaptor(curve),
                                              CreateSurface.as_adaptor(surface), tol, tol)
        index = MeasureExtrema._get_extremum_index([extrema_curve_surface.SquareDistance(i)
                                                    for i in range(1, extrema_curve_surface.NbExt() + 1)], use_smallest)

        p1 = Extrema_POnCurv()
        p2 = Extrema_POnSurf()
        extrema_curve_surface.Points(index, p1, p2)
        u_curve = p1.Parameter()
        u_surface, v_surface = p2.Parameter()
        return u_curve, u_surface, v_surface, p1.Value(), p2.Value()
