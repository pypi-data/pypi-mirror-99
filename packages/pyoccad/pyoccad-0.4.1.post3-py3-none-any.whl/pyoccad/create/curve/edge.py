from typing import Union

from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_Curve
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.GeomAPI import geomapi
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Shape, topods
from OCC.Core.gp import gp_Circ, gp_Elips, gp_Pln

from pyoccad.create import CreatePoint
from pyoccad.typing import PointT


class CreateEdge:
    """Factory to create edge curves.

    An edge is a topological entity that corresponds to 1D object – a curve.

    It may designate a face boundary (e.g. one of the twelve edges of a box) or just a ‘floating' edge not belonging to
    a face (imagine an initial contour before constructing a prism or a sweep).

    Face edges can be shared by two (or more) faces (e.g. in a stamp model they represent connection lines between
    faces) or can only belong to one face (in a stamp model these are boundary edges).

    For more information: https://opencascade.blogspot.com/2009/02/topology-and-geometry-in-open-cascade_12.html
    """
    @staticmethod
    def as_edge(edge: TopoDS_Shape) -> TopoDS_Edge:
        return topods.Edge(edge)

    @staticmethod
    def from_contour(geometry: Union[Geom_Curve, gp_Circ, gp_Elips, TopoDS_Edge]) -> TopoDS_Edge:
        """Build an edge from a base geometry type.

        Parameters
        ----------
        geometry : Union[Geom_Curve, gp_Circ, gp_Elips, TopoDS_Edge]
            The base geometry to consider for extracting the contour

        Returns
        -------
        contour : TopoDS_Edge
            The resulting edge
        """
        if isinstance(geometry, Geom_Curve):
            return BRepBuilderAPI_MakeEdge(geometry).Edge()
        if isinstance(geometry, gp_Circ):
            return BRepBuilderAPI_MakeEdge(geometry).Edge()
        if isinstance(geometry, gp_Elips):
            return BRepBuilderAPI_MakeEdge(geometry).Edge()
        if isinstance(geometry, TopoDS_Edge):
            return geometry

        raise TypeError('Not handled type "{}".'.format(type(geometry)))

    @staticmethod
    def from_2_points(p1: PointT, p2: PointT) -> TopoDS_Edge:
        """Create an edge from 2 points.

        Parameters
        ----------
        p1 : PointT
            The first point
        p2 : PointT
            The second point

        Returns
        -------
        e : TopoDS_Edge
            The resulting edge
        """
        return BRepBuilderAPI_MakeEdge(CreatePoint.as_point(p1), CreatePoint.as_point(p2)).Edge()

    @staticmethod
    def from_curve(curve: Union[Geom_Curve, Geom2d_Curve]) -> TopoDS_Edge:
        """Create an edge from a curve.

        Parameters
        ----------
        curve: Union[Geom_Curve, Geom2d_Curve]
            The input curve

        Returns
        -------
        edge: TopoDS_Edge
            The resulting edge
        """
        if isinstance(curve, Geom_Curve):
            return BRepBuilderAPI_MakeEdge(curve).Edge()
        if isinstance(curve, Geom2d_Curve):
            return CreateEdge.from_curve(Geom_Curve.DownCast(geomapi.To3d(curve, gp_Pln())))

        raise TypeError('The curve type "{}" is not handled'.format(type(curve)))

    @staticmethod
    def from_adaptor(adaptor: BRepAdaptor_Curve) -> TopoDS_Edge:
        """Create an edge from a curve adaptor.

        Parameters
        ----------
        adaptor: BRepAdaptor_Curve
            The given curve adaptor

        Returns
        -------
        edge: TopoDS_Edge
            The resulting edge
        """
        if isinstance(adaptor, BRepAdaptor_Curve):
            return adaptor.Edge()
        raise TypeError('Adaptor type "{}" not handled'.format(type(adaptor)))
