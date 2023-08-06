from typing import Iterable, Union, Sequence

from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakePolygon, \
    BRepBuilderAPI_MakeFace
from OCC.Core.Geom import Geom_Curve
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.Precision import precision
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire
from OCC.Core.gp import gp_Pln, gp_Circ, gp_Elips

from pyoccad.create import CreateCurve, CreateEdge, CreatePoint


class CreateWire:
    """A wire is a composite curve."""

    @staticmethod
    def from_element(element: Union[TopoDS_Wire, Adaptor3d_Curve,
                                    Geom_Curve, gp_Circ, gp_Elips, TopoDS_Edge]) -> TopoDS_Wire:
        """Create a wire from a single element.

        Parameters
        ----------
        element : Union[TopoDS_Wire, Adaptor3d_Curve, Geom_Curve, gp_Circ, gp_Elips, TopoDS_Edge]
            The element to convert into wire

        Returns
        -------
        w : TopoDS_Wire
            The resulting wire
        """
        if isinstance(element, TopoDS_Wire):
            return element
        if isinstance(element, (Geom_Curve, Geom2d_Curve)):
            return CreateWire.from_elements((CreateEdge.from_curve(element), ))
        if isinstance(element, Adaptor3d_Curve):
            return CreateWire.from_elements((CreateCurve.from_adaptor(element), ))
        if isinstance(element, TopoDS_Edge):
            return CreateWire.from_elements((element, ))
        if isinstance(element, (gp_Circ, gp_Elips)):
            return CreateWire.from_elements((CreateEdge.from_contour(element), ))

        raise TypeError('Element type "{}" not handled'.format(type(element)))

    @staticmethod
    def from_elements(elements: Iterable[Union[Geom_Curve, Geom2d_Curve, TopoDS_Edge,
                                               TopoDS_Wire, BRepAdaptor_Curve]]) -> TopoDS_Wire:
        """Build a wire from various elements.

        Notes
        -----
        Elements do not have to be sorted but the whole list has to be connected

        Parameters
        ----------
        elements : Sequence of Geom_Curve, Geom2d_Curve, TopoDS_Edge, TopoDS_Wire, BRepAdaptor_Curve
            The elements which shall create the wire

        Returns
        -------
        w : TopoDS_Wire
            The resulting wire
        """
        from pyoccad.explore.subshapes import ExploreSubshapes

        def _add_element_to_list(list_of_shapes, element):
            if isinstance(element, (Geom_Curve, Geom2d_Curve)):
                list_of_shapes.Append(CreateEdge.from_curve(element))
            elif isinstance(element, TopoDS_Edge):
                list_of_shapes.Append(element)
            elif isinstance(element, TopoDS_Wire):
                edges_from_wire = ExploreSubshapes.get_edges(element)
                for e in edges_from_wire:
                    list_of_shapes.Append(e)
            elif isinstance(element, (Adaptor3d_Curve, )):
                _add_element_to_list(list_of_shapes, CreateCurve.from_adaptor(element))
            else:
                raise TypeError('Element type "{}" not handled'.format(type(element)))

        list_of_shapes = TopTools_ListOfShape()
        for element in elements:
            _add_element_to_list(list_of_shapes, element)

        wire_builder = BRepBuilderAPI_MakeWire()
        wire_builder.Add(list_of_shapes)
        return wire_builder.Wire()

    @staticmethod
    def from_points(points: Sequence, auto_close: bool = False) -> TopoDS_Wire:
        """Build a polygon wire from points.

        Parameters
        ----------
        points : Sequence of containers of coordinates
            The sequence of points that define the wire

        auto_close: bool, optional
            Defines if the wire has to be automatically closed or not (default: {False})

        Returns
        -------
        w : TopoDS_Wire
            The resulting wire
        """
        polygon_builder = BRepBuilderAPI_MakePolygon()
        for p in points:
            polygon_builder.Add(CreatePoint.as_point(p))

        closing_requested = CreatePoint.as_point(points[0]).Distance(CreatePoint.as_point(points[-1])) > precision.Confusion()
        if closing_requested and auto_close:
            polygon_builder.Close()
        return polygon_builder.Wire()

    @staticmethod
    def from_plane_and_sizes(plane: gp_Pln, u_size: float, v_size: float) -> TopoDS_Wire:
        """Create a rectangular wire from a trimmed plane.

        Parameters
        ----------
        plane : gp_Pln
            Base plane to extract edge
        u_size : float
            Trim value of the plane in the u direction
        v_size : float
            Trim value of the plane in the v direction

        Returns
        -------
        wire : TopoDS_Wire
            The planar face wire
        """
        from pyoccad.explore.subshapes import ExploreSubshapes

        edges_list = ExploreSubshapes.get_edges(BRepBuilderAPI_MakeFace(plane, -u_size / 2, u_size / 2,
                                                                        -v_size / 2, v_size / 2).Face())
        return CreateWire.from_elements(edges_list)
