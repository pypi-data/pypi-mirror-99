from typing import Union

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Geom import Geom_Surface
from OCC.Core.Precision import precision
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pnt

from pyoccad.measure import MeasureCurve


class MeasureSurface:
    """Factory to measure surfaces."""

    @staticmethod
    def area(surface: Union[TopoDS_Shape, Geom_Surface]) -> float:
        """Computes a shape area

        Parameters
        ----------
        surface: Union[TopoDS_Shape, Geom_Surface]
            the surface to measure

        Returns
        -------
        area: float
            the computes area

        Raises
        ------
        TypeError
            If an unsupported type of curve is provided
        """
        if isinstance(surface, Geom_Surface):
            f = BRepBuilderAPI_MakeFace(surface, precision.Approximation()).Face()
        elif isinstance(surface, TopoDS_Shape):
            f = surface
        else:
            raise TypeError
        s_prop = GProp_GProps()
        brepgprop.SurfaceProperties(f, s_prop)
        return s_prop.Mass()

    @staticmethod
    def center(surface: Union[TopoDS_Shape, Geom_Surface]) -> gp_Pnt:
        """Compute a shape center of mass.

        Parameters
        ----------
        surface: Union[TopoDS_Shape, Geom_Surface]
            The surface to measure

        Returns
        -------
        center: gp_Pnt
            Center of mass

        Raises
        ------
        TypeError
            If the wrong type of curve is provided
        """
        if isinstance(surface, Geom_Surface):
            f = BRepBuilderAPI_MakeFace(surface, precision.Approximation()).Face()
        elif isinstance(surface, TopoDS_Shape):
            f = surface
        else:
            raise TypeError
        s_prop = GProp_GProps()
        brepgprop.SurfaceProperties(f, s_prop)
        return s_prop.CentreOfMass()

    @staticmethod
    def perimeter(surface: Union[TopoDS_Shape, Geom_Surface]) -> float:
        """Compute the total length of surface contours.

        Parameters
        ----------
        surface: Union[TopoDS_Shape, Geom_Surface]
            The surface to measure

        Returns
        -------
        perimeter: float
            The shape perimeter

        """
        from pyoccad.create import CreateTopology
        from pyoccad.explore.subshapes import ExploreSubshapes

        shape = CreateTopology.as_shape(surface)
        perimeter_ = sum([MeasureCurve.length(e) for e in ExploreSubshapes.get_edges(shape)])
        return perimeter_

    @staticmethod
    def hydraulic_diameter(surface: Union[TopoDS_Shape, Geom_Surface]) -> float:
        """Compute the hydraulic diameter of surface.

        Parameters
        ----------
        surface : Union[TopoDS_Shape, Geom_Surface]
            The surface to measure

        Returns
        -------
        diameter : float
            The face hydraulic diameter
        """
        return 4 * MeasureSurface.area(surface) / MeasureSurface.perimeter(surface)
