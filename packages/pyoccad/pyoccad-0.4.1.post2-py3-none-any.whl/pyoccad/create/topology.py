from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_HCurve
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepAdaptor import BRepAdaptor_HCurve, BRepAdaptor_HCompCurve, BRepAdaptor_Curve, BRepAdaptor_CompCurve
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeVertex, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeShell, BRepBuilderAPI_MakeSolid)
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.TopoDS import (TopoDS_Edge, TopoDS_Wire, TopoDS_Face, TopoDS_Vertex, TopoDS_Shell, TopoDS_Solid,
                             TopoDS_Compound, TopoDS_Shape, TopoDS_CompSolid)
from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Elips

from pyoccad.create import CreateCurve, CreateFace
from pyoccad.typing import PointT


class CreateTopology:
    """Factory to create topologies."""

    @staticmethod
    def as_shape(geometry ) -> TopoDS_Shape:

        if isinstance(geometry, gp_Pnt):
            return CreateTopology.make_vertex(geometry)

        if isinstance(geometry, (Geom_Curve,
                                 Adaptor3d_Curve, BRepAdaptor_Curve, BRepAdaptor_CompCurve,
                                 Adaptor3d_HCurve, BRepAdaptor_HCurve, BRepAdaptor_HCompCurve)):

            curve = CreateCurve.as_curve(geometry)
            if isinstance(curve, (TopoDS_Edge, TopoDS_Wire)):
                return curve

            return CreateTopology.make_edge(curve)

        if isinstance(geometry, (Geom_Surface, Geom_Curve, gp_Circ, gp_Elips)):
            return CreateFace.from_contour(geometry)

        if isinstance(geometry, TopoDS_Shape):
            return geometry

        raise TypeError('Type "{}" not handled.'.format(type(geometry)))

    @staticmethod
    def make_vertex(point: PointT) -> TopoDS_Vertex:
        """Build a vertex from a point.

        Parameters
        ----------
        point: PointT
            The primitive to convert

        Returns
        -------
        vertex: TopoDS_Vertex
            The resulting vertex
        """
        builder = BRepBuilderAPI_MakeVertex(point)
        vertex = builder.Vertex()
        return vertex

    @staticmethod
    def make_edge(*args) -> TopoDS_Edge:
        """Build an edge from a curve.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        edge: TopoDS_Edge
            The resulting edge
        """
        builder = BRepBuilderAPI_MakeEdge(*args)
        edge = builder.Edge()
        return edge

    @staticmethod
    def make_wire(*args) -> TopoDS_Wire:
        """Build a wire from a sequence of edges.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        wire: TopoDS_Wire
            The resulting wire
        """
        from OCC.Core.TopTools import TopTools_ListOfShape
        from OCC.Core.TopoDS import TopoDS_Edge

        builder = BRepBuilderAPI_MakeWire()
        shapes_list = TopTools_ListOfShape()
        any_edge = False

        for arg in args:
            if isinstance(arg, TopoDS_Edge):
                shapes_list.Append(arg)
                any_edge = True
            else:
                builder.Add(arg)

        if any_edge:
            builder.Add(shapes_list)

        wire = builder.Wire()
        return wire

    @staticmethod
    def make_face(*args) -> TopoDS_Face:
        """Build a face.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        face: TopoDS_Face
            The resulting face
        """
        builder = BRepBuilderAPI_MakeFace(*args)
        face = builder.Face()
        return face

    @staticmethod
    def make_shell(*args) -> TopoDS_Shell:
        """Build a shell from a collection of faces.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        shell: TopoDS_Shell
            The resulting shell
        """
        builder = BRepBuilderAPI_MakeShell(*args)
        shell = builder.Shell()
        return shell

    @staticmethod
    def make_solid(*args) -> TopoDS_Solid:
        """Build a solid from a collection of parts.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        solid: TopoDS_Solid
            The resulting solid
        """
        builder = BRepBuilderAPI_MakeSolid(*args)
        solid = builder.Solid()
        return solid

    @staticmethod
    def make_compound(*args) -> TopoDS_Compound:
        """Build a compound from a list of shapes.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        compound: TopoDS_Compound
            The resulting compound
        """
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)
        for shape in args:
            builder.Add(compound, shape)
        return compound

    def make_compsolid(*args) -> TopoDS_CompSolid:
        """Build a compsolid from a list of shapes.

        Parameters
        ----------
        args
            The primitives to convert

        Returns
        -------
        compound: TopoDS_CompSolid
            The resulting compsolid
        """
        builder = BRep_Builder()
        compsolid = TopoDS_CompSolid()
        builder.MakeCompSolid(compsolid)
        for shape in args:
            builder.Add(compsolid, shape)
        return compsolid
