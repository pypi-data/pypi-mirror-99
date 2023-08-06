from typing import Union

from OCC.Core.Adaptor2d import Adaptor2d_Curve2d, Adaptor2d_HCurve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_HCurve
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_CompCurve, BRepAdaptor_HCurve, BRepAdaptor_HCompCurve
from OCC.Core.Geom import Geom_TrimmedCurve, Geom_Curve
from OCC.Core.Geom2d import Geom2d_TrimmedCurve, Geom2d_Curve
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve, Geom2dAdaptor_HCurve
from OCC.Core.GeomAPI import geomapi
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve, GeomAdaptor_HCurve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire
from OCC.Core.gp import gp_Pln

from pyoccad.typing import CurveT, OccCurveT, CurveAdaptorT, CurveAdaptorHandlerT


class CreateCurve:

    @staticmethod
    def as_curve(curve: CurveT) -> OccCurveT:
        """Create a curve from all possible definitions.

        Parameters
        ----------
        curve : CurveT
            The curve definition

        Returns
        -------
        resulting_curve : OccCurveT
            The resulting curve as a base OpenCascade type
        """
        if isinstance(curve, (Geom_Curve, Geom2d_Curve, TopoDS_Edge, TopoDS_Wire)):
            return curve

        return CreateCurve.from_adaptor(CreateCurve.as_adaptor(curve))

    @staticmethod
    def as_adaptor(curve: CurveT) -> CurveAdaptorT:
        """Create a curve adaptor from a curve.

        An adaptor is an internal interface to ease the use of various geometries in algorithms.

        Parameters
        ----------
        curve : CurveT
            The curve to adapt

        Returns
        -------
        adaptor : CurveAdaptorT
            The curve adaptor
        """

        # Base curves
        if isinstance(curve, (Adaptor3d_Curve, Adaptor2d_Curve2d)):
            return curve
        # Adaptors
        if isinstance(curve, Geom_Curve):
            return GeomAdaptor_Curve(curve)
        if isinstance(curve, Geom2d_Curve):
            return Geom2dAdaptor_Curve(curve)
        if isinstance(curve, TopoDS_Edge):
            return BRepAdaptor_Curve(curve)
        if isinstance(curve, TopoDS_Wire):
            return BRepAdaptor_CompCurve(curve)
        # Handlers
        if isinstance(curve, Adaptor3d_HCurve):
            return curve.ChangeCurve()
        if isinstance(curve, Adaptor2d_HCurve2d):
            return curve.ChangeCurve2d()

        raise TypeError('The curve type "{}" is not supported'.format(type(curve)))

    @staticmethod
    def as_adaptor_handler(curve: CurveT) -> CurveAdaptorHandlerT:
        """Create a curve adaptor handler from a curve.

        An adaptor is an internal interface to ease the use of various geometries in algorithms.

        Parameters
        ----------
        curve : CurveT
            The curve to be transformed

        Returns
        -------
        adaptor_handler : CurveAdaptorHandlerT
            The adaptor handler
        """
        if not isinstance(curve, (Adaptor3d_Curve, Adaptor2d_Curve2d)):
            try:
                curve = CreateCurve.as_adaptor(curve)
            except TypeError:
                raise TypeError('The curve type "{}" is not supported'.format(type(curve)))

        if isinstance(curve, GeomAdaptor_Curve):
            return GeomAdaptor_HCurve(curve)
        if isinstance(curve, Geom2dAdaptor_Curve):
            return Geom2dAdaptor_HCurve(curve)
        if isinstance(curve, BRepAdaptor_Curve):
            return BRepAdaptor_HCurve(curve)
        if isinstance(curve, BRepAdaptor_CompCurve):
            return BRepAdaptor_HCompCurve(curve)

    @staticmethod
    def from_adaptor(adaptor: CurveAdaptorT) -> OccCurveT:
        """Get the original curve from its adaptor.

        Parameters
        ----------
        adaptor: CurveAdaptorT
            The curve adaptor

        Returns
        -------
        curve: OccCurveT
            The original curve
        """

        if isinstance(adaptor, Geom2dAdaptor_HCurve):
            adaptor = adaptor.ChangeCurve2d()
        if isinstance(adaptor, Geom2dAdaptor_Curve):
            return adaptor.Curve()
        if isinstance(adaptor, GeomAdaptor_Curve):
            return adaptor.Curve()
        if isinstance(adaptor, (GeomAdaptor_HCurve, BRepAdaptor_HCurve)):
            return CreateCurve.from_adaptor(adaptor.ChangeCurve())
        if isinstance(adaptor, BRepAdaptor_Curve):
            return adaptor.Edge()
        if isinstance(adaptor, BRepAdaptor_HCompCurve):
            adaptor = adaptor.ChangeCurve()
        if isinstance(adaptor, BRepAdaptor_CompCurve):
            return adaptor.Wire()

        raise TypeError('The adaptor type "{}" is not supported'.format(type(adaptor)))

    @staticmethod
    def from_2d(curve: Geom2d_Curve, plane: gp_Pln) -> Geom_Curve:
        """Convert a 2D curve into a 3D curve.

        Parameters
        ----------
        curve : Geom2d_Curve
            The curve to be converted
        plane : gp_Pln
            The plane on which the curve lies

        Returns
        -------
        curve3d : Geom_Curve
            The resulting curve
        """

        return Geom_Curve.DownCast(geomapi.To3d(curve, plane))

    @staticmethod
    def from_3d(curve: Geom_Curve, plane: gp_Pln) -> Geom2d_Curve:
        """Convert a 3D curve into a 2D curve.

        Parameters
        ----------
        curve : Geom_Curve
            The curve to be converted
        plane : gp_Pln
            The plane on which the curve should lie

        Returns
        -------
        curve2d : Geom_Curve
            The resulting curve
        """

        return Geom2d_Curve.DownCast(geomapi.To2d(curve, plane))

    @staticmethod
    def from_edge(edge: TopoDS_Edge) -> Geom_Curve:
        if isinstance(edge, TopoDS_Edge):
            c, u1, u2 = BRep_Tool.Curve(edge)
            return CreateCurve.trimmed(c, u1, u2)

    @staticmethod
    def trimmed(curve: Union[Geom_Curve, Geom2d_Curve], u1: float, u2: float) -> Union[Geom_TrimmedCurve,
                                                                                       Geom2d_TrimmedCurve]:
        """Create a trimmed curve.

        Parameters
        ----------
        curve : Union[Geom_Curve, Geom2d_Curve]
            The curve
        u1 : float
            Starting parameter
        u2 : float
            Ending parameter

        Returns
        -------
        trimmed_curve : Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]
            The trimmed curve
        """
        curve = CreateCurve.as_curve(curve)

        if isinstance(curve, Geom_Curve):
            return Geom_TrimmedCurve(curve, u1, u2)
        if isinstance(curve, Geom2d_Curve):
            return Geom2d_TrimmedCurve(curve, u1, u2)

        raise TypeError('Type "{}" not handled.'.format(type(curve)))

    @staticmethod
    def curvilinear_trimmed(curve: Union[Geom_Curve, Geom2d_Curve], m1: float, m2: float) -> Union[Geom_TrimmedCurve,
                                                                                                   Geom2d_TrimmedCurve]:
        """Create a trimmed curve according to fraction length.

        Parameters
        ----------
        curve : Union[Geom_Curve, Geom2d_Curve]
            The curve
        m1 : float
            Starting curvilinear abscissa
        m2 : float
            Ending curvilinear abscissa

        Returns
        -------
        trimmed_curve : Union[Geom_TrimmedCurve, Geom2d_TrimmedCurve]
            The trimmed curve
        """
        from pyoccad.measure import MeasureCurve

        curve = CreateCurve.as_curve(curve)
        if not isinstance(curve, (Geom_Curve, Geom2d_Curve)):
            raise TypeError('Type "{}" not handled.'.format(type(curve)))

        u1 = MeasureCurve.position_from_relative_curvilinear_abs(curve, m1)
        u2 = MeasureCurve.position_from_relative_curvilinear_abs(curve, m2)

        return CreateCurve.trimmed(curve, u1, u2)
