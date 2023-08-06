from typing import Union, Sequence

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeArcOfEllipse
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.Geom import Geom_TrimmedCurve, Geom_Ellipse
from OCC.Core.Geom2d import Geom2d_TrimmedCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt, TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt
from OCC.Core.gp import gp_Circ, gp_Circ2d, gp_Ax2, gp_Ax22d, gp_Elips

from pyoccad.create import CreateArray1


class CreateArc:
    """Factory to create an arc or curve."""

    @staticmethod
    def from_angles(axis: Union[gp_Ax2, gp_Ax22d], radius: float,
                    start_angle: float, end_angle: float, clockwise: bool = True) -> Union[Geom2d_TrimmedCurve,
                                                                                           Geom_TrimmedCurve]:
        """Create an arc rotating around an axis, with a given angular start and end.

        Parameters
        ----------
        axis : Union[gp_Ax2, gp_Ax22d]
            AxisT used to define the circle reference plane
        radius : float
            Base circle radius
        start_angle : float
            [rad] Starting angle with ax2.XDirection as reference
        end_angle : float
            [rad] Ending angle with ax2.XDirection as reference
        clockwise : bool, optional
            Defines if the reference rotation if clockwise or not (it is then counter-clockwise). Default value: True

        Returns
        -------
        arc : Union[Geom2d_TrimmedCurve, Geom_TrimmedCurve]
            The resulting arc of circle
        """
        if isinstance(axis, gp_Ax22d):
            c = gp_Circ2d(axis, radius)
            return GCE2d_MakeArcOfCircle(c, start_angle, end_angle, clockwise).Value()
        if isinstance(axis, gp_Ax2):
            c = gp_Circ(axis, radius)
            return GC_MakeArcOfCircle(c, start_angle, end_angle, clockwise).Value()

        raise TypeError('Type of axis should be one of (gp_Ax2, gp_Ax22d), got "{}"'.format(type(axis)))

    @staticmethod
    def from_3_points(points: Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt,
                                    TColgp_Array1OfPnt2d, TColgp_Array1OfPnt,
                                    Sequence]) -> Union[Geom2d_TrimmedCurve, Geom_TrimmedCurve]:
        """Create an arc of circle between p1 and p3, passing by p2 inbetween.

        Parameters
        ----------
        points : Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array1OfPnt,
        Sequence]
            The list of the 3 points

        Returns
        -------
        arc : {Geom2d_TrimedCurve, Geom_TrimedCurve}
            the arc of circle

        Raises
        ------
        TypeError
            If the points provided do not respect expected types
        """
        if isinstance(points, (Sequence, TColgp_HArray1OfPnt, TColgp_HArray1OfPnt2d)):
            points = CreateArray1.of_points(points)

        if isinstance(points, TColgp_Array1OfPnt2d):
            return GCE2d_MakeArcOfCircle(points.Value(1),
                                         points.Value(2),
                                         points.Value(3)).Value()
        if isinstance(points, TColgp_Array1OfPnt):
            return GC_MakeArcOfCircle(points.Value(1),
                                      points.Value(2),
                                      points.Value(3)).Value()

        raise TypeError('Points do not respect expected types. Please refer to documentation.')

    @staticmethod
    def from_ellipse(ellipse: Union[gp_Elips, Geom_Ellipse],
                     start_angle: float,
                     end_angle: float,
                     clockwise: bool = True) -> Geom_TrimmedCurve:
        """Create an arc of ellipse from a complete one.

        Parameters
        ----------
        ellipse: Union[gp_Elips, Geom_Ellipse]
            The reference ellipse
        start_angle : float
            [rad] Starting angle parameter
        end_angle : float
            [rad] Ending angle parameter
        clockwise : bool, optional
            Whether the reference rotation if clockwise or not {Default=True}

        Returns
        -------
        arc : Geom_TrimmedCurve
            The resulting arc of ellipse
        """
        if isinstance(ellipse, Geom_Ellipse):
            ellipse_ = ellipse.Elips()
        else:
            ellipse_ = ellipse

        return GC_MakeArcOfEllipse(ellipse_, start_angle, end_angle, clockwise).Value()
