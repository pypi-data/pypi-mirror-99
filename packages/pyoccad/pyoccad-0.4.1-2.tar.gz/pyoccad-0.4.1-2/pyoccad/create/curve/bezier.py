from typing import Union, Sequence

import numpy as np
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.Geom2d import Geom2d_BezierCurve
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_HArray1OfReal
from OCC.Core.TColgp import (TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt)

from pyoccad.create import CreatePoint, CreateVector, CreateArray1
from pyoccad.create.control_point import ControlPoint
from pyoccad.typing import PointT


class CreateBezier:
    """Factory to create Bezier curves.

    A Bezier curve is a parametric curve used in computer graphics and related fields.
    The curve, which is related to the Bernstein polynomial, is named after Pierre Bezier, who used it in \
    the 1960s for designing curves for the bodywork of Renault cars.

    Other uses include the design of computer fonts and animation.
    Bezier curves can be combined to form a Bezier spline, or generalized to higher dimensions to form Bezier surfaces.
    """

    @staticmethod
    def from_poles(poles: Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt,
                                TColgp_Array1OfPnt2d, TColgp_Array1OfPnt, Sequence[PointT]],
                   weights: Union[TColStd_Array1OfReal, TColStd_HArray1OfReal,
                                  Sequence[float]] = None) -> Union[Geom_BezierCurve, Geom2d_BezierCurve]:
        """Creates a Bezier 2D/3D curve from a list of poles

        Parameters
        ----------
        poles : Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array1OfPnt,
                      Sequence[PointT]]
            The list of poles

        weights : Union[TColStd_Array1OfReal, TColStd_HArray1OfReal, Sequence[float]], optional
            The weights of the poles. Default None resulting in all poles having a weight of 1.

        Returns
        -------
        bezier_curve : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve

        Raises
        ------
        TypeError
            If the poles provided do not respect expected types

        """
        if isinstance(poles, (Sequence, TColgp_HArray1OfPnt, TColgp_HArray1OfPnt2d)):
            poles = CreateArray1.of_points(poles)

        if isinstance(weights, (TColStd_HArray1OfReal, Sequence)):
            weights = CreateArray1.of_floats(weights)

        if weights is None:
            args = (poles, )
        else:
            args = (poles, weights)

        if isinstance(poles, TColgp_Array1OfPnt2d):
            return Geom2d_BezierCurve(*args)
        if isinstance(poles, TColgp_Array1OfPnt):
            return Geom_BezierCurve(*args)

        raise TypeError('Poles type "{}" is incorrect'.format(type(poles)))

    @staticmethod
    def from_control_points(control_points: Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt,
                                                  TColgp_Array1OfPnt2d, TColgp_Array1OfPnt,
                                                  Sequence]) -> Union[Geom_BezierCurve, Geom2d_BezierCurve]:
        """Creates a Bezier 2D/3D curve from a list of control points

        The resulting curve will pass at the control points with the specified derivatives if provided.

        Notes
        -----
        The control point class is defined in the pyoccad.create.point module

        Parameters
        ----------
        control_points : Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array1OfPnt,
        Sequence]
            The list of control points

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve

        Raises
        ------
        TypeError
            If the control points provided do not respect expected types

        """

        for cp in control_points:
            if not isinstance(cp, ControlPoint):
                raise TypeError('Type pyoccad.create.point.ControlPoint expected, got type "{}"'.format(type(cp)))

        # TODO: extend this method! only works for 2 control points and only first derivative
        if len(control_points) != 2:
            raise NotImplementedError('Only case with 2 control points is handled for the moment, '
                                      'got {}'.format(len(control_points)))
        if any([cp.has_d2 for cp in control_points]):
            raise NotImplementedError('Control points curvature is not handled yet.')

        poles = [CreatePoint.as_point(cp.Coord()) for cp in control_points]
        if control_points[0].has_d1:
            cp = control_points[0]
            poles.insert(1, CreatePoint.as_point(np.array(CreatePoint.as_list(cp.Coord())) +
                                                 np.array(CreateVector.as_list(cp.d1)) / 3))

        if control_points[1].has_d1:
            cp = control_points[1]
            poles.insert(2, CreatePoint.as_point(np.array(CreatePoint.as_list(cp.Coord())) -
                                                 np.array(CreateVector.as_list(cp.d1)) / 3))

        return CreateBezier.from_poles(poles)

    @staticmethod
    def connecting_curves(crv1, crv2, u1, u2, tension1, tension2):
        """Connects 2 curves with a Bezier at given positions, with given tensions

        Parameters
        ----------
        crv1 : {Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve}
            the first curve
        crv2 : {Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve}
            the second curve
        u1 : float
            the crv1 parameter where connection shall be made with crv1
        u2 : float
            the crv2 parameter where connection shall be made with crv2
        tension1 : float
            the weight to apply on crv1 side on the tangent vector at the connection point
        tension2 : float
            the weight to apply on crv2 side on the tangent vector at the connection point

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve

        """
        from pyoccad.measure import MeasureCurve

        p1, v1 = MeasureCurve.derivatives(crv1, u1, 1)
        p2, v2 = MeasureCurve.derivatives(crv2, u2, 1)
        return CreateBezier.from_poles([p1, p1.Translated(v1 * tension1), p2.Translated(-v2 * tension2), p2])

    @staticmethod
    def c1_connecting_curves(crv1, crv2, u1, u2):
        """Connects 2 curves with a Bezier at given positions, with C1 continuity

        Parameters
        ----------
        crv1 : {Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve}
            the first curve
        crv2 : {Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve}
            the second curve
        u1 : float
            the crv1 parameter where connection shall be made with crv1
        u2 : float
            the crv2 parameter where connection shall be made with crv2

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve
        """
        return CreateBezier.connecting_curves(crv1, crv2, u1, u2, 1. / 3., 1. / 3.)

    @staticmethod
    def c1_connecting_curves_end_start(crv1, crv2):
        """Connects 2 curves with a Bezier, with C1 continuity

        Notes
        -----
        crv1 point is taken at the end of the curve, and crv2 point at the start.

        Parameters
        ----------
        crv1 : {Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve}
            the first curve
        crv2 : {Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve}
            the second curve

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve
        """
        return CreateBezier.c1_connecting_curves(crv1, crv2, crv1.LastParameter(), crv2.FirstParameter())

    @staticmethod
    def tangent_c0_continuity(start_pt, end_pt, start_d1, end_d1):
        """Creates a bezier between two points with direction imposed on the two points

        Parameters
        ----------
        start_pt : {container of coordinates}
            the starting point
        end_pt : {container of coordinates}
            the ending point
        start_d1 : {container of coordinates}
            the required first derivative direction at curve starting point
        end_d1 : {container of coordinates}
            the required first derivative direction at curve ending point

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve
        """
        poles = [
            start_pt,
            np.array(start_pt) + np.array(start_d1) / 3,
            np.array(end_pt) - np.array(end_d1) / 3,
            end_pt
        ]
        return CreateBezier.from_poles(poles)

    @staticmethod
    def g1_absolute_tension(start, end, start_d1, end_d1, start_tension, end_tension):
        """Create a tangent bezier curve with G1 continuity.

        Parameters
        ----------
        start : {container of coordinates}
            the starting point
        end : {container of coordinates}
            the ending point
        start_d1 : {container of coordinates}
            the required first derivative direction at curve starting point
        end_d1 : {container of coordinates}
            the required first derivative direction at curve ending point
        start_tension : {container of coordinates}
            the required first derivative norm at curve starting point
        end_tension : {container of coordinates}
            the required first derivative norm at curve ending point

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve
        """
        poles = [
            start,
            np.array(start) + np.array(start_d1) / np.linalg.norm(start_d1) * start_tension / 3,
            np.array(end) - np.array(end_d1) / np.linalg.norm(end_d1) * end_tension / 3,
            end
        ]
        return CreateBezier.from_poles(poles)

    @staticmethod
    def g1_relative_tension(start, end, start_d1, end_d1, start_tension, end_tension):
        """Create a tangent bezier curve with G1 continuity.
        The relative tensions refers to the distance between starting and ending points.

        Parameters
        ----------
        start : {container of coordinates}
            the starting point
        end : {container of coordinates}
            the ending point
        start_d1 : {container of coordinates}
            the required first derivative direction at curve starting point
        end_d1 : {container of coordinates}
            the required first derivative direction at curve ending point
        start_tension : {container of coordinates}
            the required first derivative relative norm at curve starting point
        end_tension : {container of coordinates}
            the required first derivative relative norm at curve ending point

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve
        """
        ref = np.linalg.norm(np.array(start) - np.array(end))
        poles = [
            start,
            np.array(start) + np.array(start_d1) / np.linalg.norm(start_d1) * start_tension * ref / 3,
            np.array(end) - np.array(end_d1) / np.linalg.norm(end_d1) * end_tension * ref / 3,
            end
        ]
        return CreateBezier.from_poles(poles)

    @staticmethod
    def c1_continuity(start, end, start_d1, end_d1):
        """Create a tangent bezier curve with C1 continuity.

        Parameters
        ----------
        start : {container of coordinates}
            the starting point
        end : {container of coordinates}
            the ending point
        start_d1 : {container of coordinates}
            the required first derivative at curve starting point
        end_d1 : {container of coordinates}
            the required first derivative at curve ending point

        Returns
        -------
        b : {Geom_BezierCurve, Geom2d_BezierCurve}
            The resulting bezier curve
        """
        poles = [
            start,
            np.array(start) + np.array(start_d1) / 3,
            np.array(end) - np.array(end_d1) / 3,
            end
        ]
        return CreateBezier.from_poles(poles)
