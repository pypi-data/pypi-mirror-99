from typing import Union, Iterable

from OCC.Core.Adaptor2d import Adaptor2d_Curve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_HCurve
from OCC.Core.GCPnts import GCPnts_AbscissaPoint
from OCC.Core.Geom2dLProp import Geom2dLProp_CLProps2d
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.LProp3d import LProp3d_CLProps
from OCC.Core.Precision import precision
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Dir, gp_Dir2d, gp_Vec

from pyoccad.measure import MeasurePoint
from pyoccad.typing import CurveT, PointT, DirectionT


class MeasureCurve:

    @staticmethod
    def dimension(curve: CurveT) -> int:
        """Return the dimension (2 or 3) or a curve.

        Notes
        -----
        This operation is performed by measuring the dimension of the first point of the curve

        Parameters
        ----------
        curve: CurveT
            The curve to be measured

        Returns
        -------
        dimension: int
            The dimension of the curve

        """
        p = curve.Value(curve.FirstParameter())
        return MeasurePoint.dimension(p)

    @staticmethod
    def unique_dimension(curves: Iterable[CurveT]) -> int:
        dimensions = [MeasureCurve.dimension(curve) for curve in curves]
        if len(set(dimensions)) > 1:
            raise TypeError('Curves should all have the same dimension, got dimensions {}.'.format(dimensions))

        return dimensions[0]

    @staticmethod
    def value(curve, parameter):
        return curve.Value(parameter)

    @staticmethod
    def derivatives(curve, parameter, order):
        from pyoccad.create.point import CreatePoint

        if order == 0:
            return curve.Value(parameter)
        if order == 1:
            p1 = CreatePoint.as_point((0., 0., 0.))
            v1 = gp_Vec()
            curve.D1(parameter, p1, v1)
            return [p1, v1]
        if order == 2:
            p1 = CreatePoint.as_point((0., 0., 0.))
            v1 = gp_Vec()
            v2 = gp_Vec()
            curve.D2(parameter, p1, v1, v2)
            return [p1, v1, v2]
        if order == 3:
            p1 = CreatePoint.as_point((0., 0., 0.))
            v1 = gp_Vec()
            v2 = gp_Vec()
            v3 = gp_Vec()
            curve.D3(parameter, p1, v1, v2, v3)
            return [p1, v1, v2, v3]

        return [curve.Value(parameter)] + [curve.DN(parameter, o) for o in range(1, order+1)]

    @staticmethod
    def length(curve: CurveT, tolerance: float = precision().Confusion()) -> float:
        """Compute the length of a curve.

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        tolerance: float, optional
            The tolerance of the length computation

        Returns
        -------
        length: float
            The curve length
        """
        from pyoccad.create.curve.curve import CreateCurve

        if not isinstance(curve, (Adaptor3d_Curve, Adaptor2d_Curve2d)):
            curve = CreateCurve.as_adaptor(curve)

        return GCPnts_AbscissaPoint().Length(curve, tolerance)

    @staticmethod
    def fraction_length(curve: CurveT, u1: float, u2: float, tolerance: float = precision().Confusion()) -> float:
        """Compute the length of a curve fraction defined by parametric start and end.

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        u1: float
            The starting parameter
        u2: float
            The ending parameter
        tolerance: float, optional
            The tolerance of the length computation

        Returns
        -------
        l: float
            The curve length between parameters u1 and u2
        """
        from pyoccad.create.curve.curve import CreateCurve

        if not isinstance(curve, (Adaptor3d_Curve, Adaptor2d_Curve2d)):
            curve = CreateCurve.as_adaptor(curve)

        return GCPnts_AbscissaPoint().Length(curve, u1, u2, tolerance)

    @staticmethod
    def position_from_relative_curvilinear_abs_with_start(curve: CurveT, m, u1,
                                                          tolerance: float = precision().Confusion()) -> float:
        """Compute curve's parameter corresponding to the given relative curvilinear abscissa from the given parameter

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        m: float
            Relative curvilinear abscissa
        u1: float
            Starting position on curve
        tolerance: float, optional
            The tolerance of the length computation

        Returns
        -------
        u: float
            The position
        """
        from pyoccad.create.curve.curve import CreateCurve

        if not isinstance(curve, (Adaptor3d_Curve, Adaptor2d_Curve2d)):
            curve = CreateCurve.as_adaptor(curve)

        return GCPnts_AbscissaPoint(tolerance, curve, m * MeasureCurve.length(curve, tolerance), u1).Parameter()

    @staticmethod
    def position_from_relative_curvilinear_abs(curve: CurveT, m, tol=precision().Confusion()):
        """Compute curve's parameter corresponding to the given relative curvilinear abscissa.

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        m: float
            Relative curvilinear abscissa
        tol: float, optional
            The tolerance of the length computation

        Returns
        -------
        u: float
            The position
        """
        return MeasureCurve.position_from_relative_curvilinear_abs_with_start(curve, m, curve.FirstParameter(), tol)

    @staticmethod
    def __build_clprops(curve: CurveT, u: float,
                        tol=precision().Confusion()) -> Union[Geom2dLProp_CLProps2d, LProp3d_CLProps]:
        """Generate a measurement tool for both 2D and 3D curves.

        Parameters
        ----------
        curve: CurveT
            The curve to measure
        u: float
            Initializes the local properties of the curve for this parameter
        tol:
            The linear tolerance, used to test if a vector is null

        Returns
        -------
        tool: Union[Geom2dLProp_CLProps2d, LProp3d_CLProps]
            The measurement tool
        """
        from pyoccad.create.curve.curve import CreateCurve

        curve_adaptor_handler = CreateCurve.as_adaptor_handler(curve)

        if isinstance(curve_adaptor_handler, Adaptor3d_HCurve):
            cl_props = LProp3d_CLProps(curve_adaptor_handler, u, 2, tol)
        else:  # Geom2dAdaptor_HCurve
            cl_props = Geom2dLProp_CLProps2d(curve_adaptor_handler.ChangeCurve2d().Curve(), u, 2, tol)

        return cl_props

    @staticmethod
    def center_of_curvature(curve: CurveT, u, tol=precision().Confusion()) -> PointT:
        """Return the center of curvature.

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        u: float
            Parameter where the analysis shall be performed
        tol: float, optional
            The tolerance of the length computation

        Returns
        -------
        pc: PointT
            Center of curvature
        """
        cl_props = MeasureCurve.__build_clprops(curve, u, tol)
        if isinstance(cl_props, LProp3d_CLProps):
            pc = gp_Pnt()
            cl_props.CentreOfCurvature(pc)
        else:
            pc = gp_Pnt2d()
            cl_props.CentreOfCurvature(pc)
        return pc

    @staticmethod
    def curvature(curve: CurveT, u, tol=precision().Confusion()) -> float:
        """Return the local curvature value.

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        u: float
            Parameter where the analysis shall be performed
        tol: float, optional
            The tolerance of the length computation

        Returns
        -------
        curvature: float
            The curvature
        """
        cl_props = MeasureCurve.__build_clprops(curve, u, tol)
        return cl_props.Curvature()

    @staticmethod
    def tangent(curve: CurveT, u, tol=precision().Confusion()) -> DirectionT:
        """Return the local tangent direction.

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        u: float
            Parameter where the analysis shall be performed
        tol: float, optional
            The tolerance of the length computation

        Returns
        -------
        tangent: DirectionT
            Tangent direction
        """
        cl_props = MeasureCurve.__build_clprops(curve, u, tol)
        if isinstance(cl_props, LProp3d_CLProps):
            tangent_ = gp_Dir()
            cl_props.Tangent(tangent_)
        else:
            tangent_ = gp_Dir2d()
            cl_props.Tangent(tangent_)
        return tangent_

    @staticmethod
    def normal(curve: CurveT, u, tol=precision().Confusion()) -> DirectionT:
        """returns local normal direction

        Parameters
        ----------
        curve: CurveT
            The curve to be measured
        u: float
            Parameter where the analysis shall be performed
        tol: float, optional
            The tolerance of the length computation

        Returns
        -------
        normal: DirectionT
            The normal direction
        """
        cl_props = MeasureCurve.__build_clprops(curve, u, tol)
        if isinstance(cl_props, LProp3d_CLProps):
            normal_ = gp_Dir()
            cl_props.Normal(normal_)
        else:
            normal_ = gp_Dir2d()
            cl_props.Normal(normal_)
        return normal_

    @staticmethod
    def parameter_from_point(curve: CurveT, point: PointT, tol: float = precision().Confusion()) -> float:
        """Get the parameter on a curve from a point on it.

        Parameters
        ----------
        curve: CurveT
            The curve
        point: PointT
            The point
        tol: float, optional
            The tolerance for the distance between the point and the curve {default=precision().Confusion()}

        Returns
        -------
        parameter: float
            The parameter corresponding to the point
        """
        projection = GeomAPI_ProjectPointOnCurve(curve, point)

        if projection.LowerDistance() < tol:
            return projection.LowerDistanceParameter()

        raise RuntimeError('The point is not on the curve.')
