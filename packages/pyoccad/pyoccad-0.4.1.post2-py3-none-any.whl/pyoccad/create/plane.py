from OCC.Core.gp import gp_Pln, gp_Dir, gp_Ax3

from pyoccad.create import CreatePoint, CreateDirection
from pyoccad.typing import PointT, CurveT, DirectionT, Axis3T


class CreatePlane:
    """Factory to create planes."""
    # TODO: extend reversed planes

    @staticmethod
    def xpy(point: PointT) -> gp_Pln:
        """Create a plane containing a point p parallel to xOy.
        
        Parameters
        ----------
        point: PointT
            The point
    
        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        ax3 = gp_Ax3(CreatePoint.as_point(point), gp_Dir(0, 0, 1), gp_Dir(1, 0, 0))
        return gp_Pln(ax3)

    @staticmethod
    def zpx(point: PointT) -> gp_Pln:
        """Create a plane containing a point p parallel to xOz.

        Parameters
        ----------
        point: PointT
            The point

        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        ax3 = gp_Ax3(CreatePoint.as_point(point), gp_Dir(0, 1, 0), gp_Dir(0, 0, 1))
        return gp_Pln(ax3)

    @staticmethod
    def ypz(point: PointT) -> gp_Pln:
        """Create a plane containing a point p parallel to yOz.

        Parameters
        ----------
        point: PointT
            The point

        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        ax3 = gp_Ax3(CreatePoint.as_point(point), gp_Dir(1, 0, 0), gp_Dir(0, 1, 0))
        return gp_Pln(ax3)

    @staticmethod
    def zpy(point: PointT) -> gp_Pln:
        """Create a plane containing a point p parallel to zOy.

        Parameters
        ----------
        point: PointT
            The point

        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        ax3 = gp_Ax3(CreatePoint.as_point(point), gp_Dir(-1, 0, 0), gp_Dir(0, 0, 1))
        return gp_Pln(ax3)

    @staticmethod
    def xoy() -> gp_Pln:
        """Creates a x0y plane.
    
        Returns
        -------
        plane : gp_Pln
            The resulting plane
        """
        return CreatePlane.xpy([0., 0., 0.])

    @staticmethod
    def zox() -> gp_Pln:
        """Creates a z0x plane.

        Returns
        -------
        plane : gp_Pln
            The resulting plane
        """
        return CreatePlane.zpx([0., 0., 0.])

    @staticmethod
    def yoz() -> gp_Pln:
        """Creates a y0x plane.

        Returns
        -------
        plane : gp_Pln
            The resulting plane
        """
        return CreatePlane.ypz([0., 0., 0.])

    @staticmethod
    def zoy() -> gp_Pln:
        """Creates a z0y plane.

        Returns
        -------
        plane : gp_Pln
            The resulting plane
        """
        return CreatePlane.zpy([0., 0., 0.])

    @staticmethod
    def normal_to_curve_at_position(curve: CurveT, u: float) -> gp_Pln:
        """Create a plane normal to a curve at a given position.
        
        Parameters
        ----------
        curve: CurveT
            The curve
        u: float
            The parameter where the normal is computed
        
        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        from pyoccad.measure import MeasureCurve

        p, t = MeasureCurve.derivatives(curve, u, 1)
        return gp_Pln(p, CreateDirection.as_direction(t))

    @staticmethod
    def normal_to_curve_with_xdir(curve: CurveT, u: float, x_direction: DirectionT) -> gp_Pln:
        """Create a plane normal to a curve at a given position, with the plane x-direction specified.
        
        Parameters
        ----------
        curve: CurveT
            The curve
        u: float
            The parameter where the normal is computed
        x_direction: DirectionT
            The requested direction for the x-axis of the plane

        Returns
        -------
        plane: gp_Pln
              The resulting plane
        """
        from pyoccad.measure import MeasureCurve

        p, t = MeasureCurve.derivatives(curve, u, 1)
        return gp_Pln(gp_Ax3(p, CreateDirection.as_direction(t), CreateDirection.as_direction(x_direction)))

    @staticmethod
    def normal_to_curve_at_fraction(curve: CurveT, m: float) -> gp_Pln:
        """Create a plane normal to a curve at a given fraction.

        Parameters
        ----------
        curve: CurveT
            The curve
        m: float
            The curve fraction

        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        from pyoccad.measure import MeasureCurve

        u = MeasureCurve.position_from_relative_curvilinear_abs(curve, m)
        return CreatePlane.normal_to_curve_at_position(curve, u)

    @staticmethod
    def from_axis(axis: Axis3T) -> gp_Pln:
        """Create a plane from axis.

        Parameters
        ----------
        axis: AxisT
            The axis

        Returns
        -------
        plane: gp_Pln
            The resulting plane
        """
        return gp_Pln(axis.Location(), axis.Direction())
