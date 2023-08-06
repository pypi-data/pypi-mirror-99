from math import pi
from typing import Union

from OCC.Core.Adaptor2d import Adaptor2d_Curve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.GC import GC_MakeLine, GC_MakeSegment
from OCC.Core.GCE2d import GCE2d_MakeLine, GCE2d_MakeSegment
from OCC.Core.Geom import Geom_Line, Geom_Curve, Geom_TrimmedCurve
from OCC.Core.Geom2d import Geom2d_Line, Geom2d_TrimmedCurve, Geom2d_Curve
from OCC.Core.gp import gp_Vec, gp_Pnt, gp_Vec2d, gp_Pnt2d, gp_Dir2d, gp_Dir, gp_Lin, gp_Lin2d

from pyoccad.create import CreateDirection, CreateIntersection, CreatePoint
from pyoccad.typing import AxisT, DirectionT, PointT


class CreateLine:
    """Factory to create line curves."""

    @staticmethod
    def from_axis(axis_: AxisT) -> Geom_Line:
        """Build a line from an axis.

        Parameters
        ----------
        axis_: AxisT
            The reference axis

        Returns
        -------
        line: Geom_Line
            The resulting line
        """
        return GC_MakeLine(axis_).Value()

    @staticmethod
    def from_point_and_direction(point: PointT, direction: DirectionT) -> Union[Geom_Line, Geom2d_Line]:
        """Build a line from a point and a direction.

        Parameters
        ----------
        point: PointT
            The point
        direction: DirectionT
            The direction

        Returns
        -------
        l : Union[Geom_Line, Geom2d_Line]
            the line
        """
        point_ = CreatePoint.as_point(point)
        direction_ = CreateDirection.as_direction(direction)

        if isinstance(point_, gp_Pnt) and isinstance(direction_, gp_Dir):
            return GC_MakeLine(point_, direction_).Value()
        if isinstance(point_, gp_Pnt2d) and isinstance(direction_, gp_Dir2d):
            return GCE2d_MakeLine(point_, direction_).Value()

        raise TypeError('PointT and direction should be (gp_Pnt, gp_Dir) or (gp_Pnt2d, gp_Dir2d), '
                        'got ({}, {}).'.format(type(point_), type(direction_)))

    @staticmethod
    def tangent_to_curve(curve: Union[Geom_Curve, Adaptor3d_Curve,
                                      Geom2d_Curve, Adaptor2d_Curve2d], u: float) -> Union[Geom_Line, Geom2d_Line]:
        """Build a line tangent to curve at a given position.

        Parameters
        ----------
        curve : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The curve
        u : float
            The parameter defining the position on the curve

        Returns
        -------
        line : Union[Geom_Line, Geom2d_Line]
            The resulting line
        """
        from pyoccad.measure import MeasureCurve

        dimension = MeasureCurve.dimension(curve)
        if dimension == 3:
            p = gp_Pnt()
            t = gp_Vec()
            curve.D1(u, p, t)
            line = GC_MakeLine(p, gp_Dir(t)).Value()
        else:  # dimension == 2
            p = gp_Pnt2d()
            t = gp_Vec2d()
            curve.D1(u, p, t)
            line = GCE2d_MakeLine(p, gp_Dir2d(t)).Value()

        return line

    @staticmethod
    def through_2_points(p1: PointT, p2: PointT) -> Union[Geom_Line, Geom2d_Line]:
        """Build a line through 2 points.

        Parameters
        ----------
        p1 : PointT
            The first point
        p2 : float
            The second point

        Returns
        -------
        line : Union[Geom_Line, Geom2d_Line]
            The resulting line
        """
        from pyoccad.measure import MeasurePoint

        dimension = MeasurePoint.unique_dimension((p1, p2))

        if dimension == 3:
            d = gp_Dir(CreatePoint.as_point(p2).XYZ() - CreatePoint.as_point(p1).XYZ())
            return Geom_Line(gp_Lin(CreatePoint.as_point(p1), d))
        else:  # dimension == 2
            d = gp_Dir2d(CreatePoint.as_point(p2).XY() - CreatePoint.as_point(p1).XY())
            return Geom2d_Line(gp_Lin2d(CreatePoint.as_point(p1), d))

    @staticmethod
    def between_2_points(p1: PointT, p2: PointT) -> Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]:
        """Build a segment between 2 points.

        Parameters
        ----------
        p1 : PointT
            The first point
        p2 : float
            The second point

        Returns
        -------
        segment : Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]
            The resulting segment as a trimmed curve
        """
        from pyoccad.measure import MeasurePoint

        dimension = MeasurePoint.unique_dimension((p1, p2))

        if dimension == 3:
            return GC_MakeSegment(CreatePoint.as_point(p1), CreatePoint.as_point(p2)).Value()
        else:  # dimension == 2
            return GCE2d_MakeSegment(CreatePoint.as_point(p1), CreatePoint.as_point(p2)).Value()

    @staticmethod
    def between_2_curves_at_positions(curve1: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d],
                                      curve2: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d],
                                      u1: float,
                                      u2: float) -> Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]:
        """Build a segment between 2 curves at given positions.

        Parameters
        ----------
        curve1 : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The first curve
        curve2 : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The second curve
        u1 : float
            The parameter defining the position on the first curve
        u2 : float
            The parameter defining the position on the second curve

        Returns
        -------
        segment : Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]
            The resulting segment as a trimmed curve
        """
        from pyoccad.measure import MeasureCurve

        dimension = MeasureCurve.unique_dimension((curve1, curve2))

        if dimension == 3:
            return GC_MakeSegment(curve1.Value(u1), curve2.Value(u2)).Value()
        else:  # dimension == 2
            return GCE2d_MakeSegment(curve1.Value(u1), curve2.Value(u2)).Value()

    @staticmethod
    def between_2_curves_starts(curve1: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d],
                                curve2: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
                                ) -> Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]:
        """Build a segment between 2 curves at start positions.

        Parameters
        ----------
        curve1 : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The first curve
        curve2 : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The second curve

        Returns
        -------
        segment : Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]
            The resulting segment as a trimmed curve
        """
        u1 = curve1.FirstParameter()
        u2 = curve2.FirstParameter()
        return CreateLine.between_2_curves_at_positions(curve1, curve2, u1, u2)

    @staticmethod
    def between_2_curves_ends(curve1: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d],
                              curve2: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
                              ) -> Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]:
        """Build a segment between 2 curves at end positions.

        Parameters
        ----------
        curve1 : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The first curve
        curve2 : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The second curve

        Returns
        -------
        segment : Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]
            The resulting segment as a trimmed curve
        """
        u1 = curve1.LastParameter()
        u2 = curve2.LastParameter()
        return CreateLine.between_2_curves_at_positions(curve1, curve2, u1, u2)

    @staticmethod
    def normal_to_curve(curve: Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d],
                        u: float,
                        plane_direction: DirectionT = gp_Dir(0., 0., 1.)) -> Union[Geom_Line, Geom2d_Line]:
        """Build a line normal to curve at a given position in a plane defined by its direction/normal.

        Parameters
        ----------
        curve : Union[Geom_Curve, Adaptor3d_Curve, Geom2d_Curve, Adaptor2d_Curve2d]
            The curve
        u : float
            The parameter defining the position on the curve
        plane_direction : gp_Dir
            The direction defining the plane, in case of 3D curve only {default=(0., 0., 1.)}

        Returns
        -------
        line : Union[Geom_Line, Geom2d_Line]
            The resulting line
        """
        from pyoccad.measure import MeasureCurve

        dimension = MeasureCurve.dimension(curve)

        if dimension == 3:
            p = gp_Pnt()
            t = gp_Vec()
            curve.D1(u, p, t)
            n = t.Crossed(gp_Vec(CreateDirection.as_direction(plane_direction)))
            return GC_MakeLine(p, gp_Dir(n)).Value()
        else:  # dimension == 2
            p = gp_Pnt2d()
            t = gp_Vec2d()
            curve.D1(u, p, t)
            n = t.Rotated(pi / 2.)
            return GCE2d_MakeLine(p, gp_Dir2d(n)).Value()

    @staticmethod
    def between_point_and_curve_at_position(point: PointT,
                                            direction: DirectionT,
                                            curve: Union[Geom2d_Curve, Adaptor2d_Curve2d],
                                            tol: float = 1e-10) -> Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]:
        """Create a segment from a point to a curve with a given direction.

        Parameters
        ----------
        point : PointT
            The point
        direction : DirectionT
            The direction
        curve : Union[Geom2d_Curve, Adaptor2d_Curve2d]
            The curve
        tol : float, optional
            The tolerance for algorithm {default=1e-10}

        Returns
        -------
        segment:  Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve], float]
            The segment and the parameter defining the point on the curve
        """
        line = CreateLine.from_point_and_direction(point, direction)
        curve_point = CreateIntersection.between_2_curves(line, curve, tol)
        return CreateLine.between_2_points(point, curve_point)
