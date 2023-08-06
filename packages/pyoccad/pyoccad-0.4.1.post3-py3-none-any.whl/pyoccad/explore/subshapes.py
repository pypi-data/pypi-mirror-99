from typing import Union, List, Iterable

from OCC.Core.ShapeAnalysis import ShapeAnalysis_Edge
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_EDGE, TopAbs_FACE, TopAbs_WIRE, TopAbs_SOLID, TopAbs_SHELL, \
    TopAbs_COMPOUND, TopAbs_COMPSOLID
from OCC.Core.TopExp import topexp
from OCC.Core.TopTools import TopTools_IndexedMapOfShape
from OCC.Core.TopoDS import topods, TopoDS_Shape, TopoDS_Edge, \
    topods_Vertex, topods_Edge, topods_Wire, topods_Face, topods_Shell, topods_Solid, topods_CompSolid, topods_Compound

SHAPE_TYPES = {'vertex': (TopAbs_VERTEX, topods_Vertex),
               'edge': (TopAbs_EDGE, topods_Edge),
               'wire': (TopAbs_WIRE, topods_Wire),
               'face': (TopAbs_FACE, topods_Face),
               'shell': (TopAbs_SHELL, topods_Shell),
               'solid': (TopAbs_SOLID, topods_Solid),
               'compsolid': (TopAbs_COMPSOLID, topods_CompSolid),
               'compound': (TopAbs_COMPOUND, topods_Compound)}

TopAbs_SHAPE = Union[topods_Vertex, topods_Edge, topods_Wire, topods_Face, topods_Shell,
                     topods_Solid, topods_CompSolid, topods_Compound]


class ExploreSubshapes:
    """Geometric module allowing the navigation though shapes to extract subshapes (solids, faces, edges, etc.)"""

    @staticmethod
    def cast_shape(shape: TopoDS_Shape, shape_type: Union[str, TopAbs_SHAPE]) -> TopoDS_Shape:
        """Cast a shape to a given type.

        Notes
        -----
        The dictionary is defined as follows:
            * 'vertex': (TopAbs_VERTEX, topods_Vertex),
            * 'edge': (TopAbs_EDGE, topods_Edge),
            * 'wire': (TopAbs_WIRE, topods_Wire),
            * 'face': (TopAbs_FACE, topods_Face),
            * 'shell': (TopAbs_SHELL, topods_Shell),
            * 'solid': (TopAbs_SOLID, topods_Solid),
            * 'compsolid': (TopAbs_COMPSOLID, topods_CompSolid),
            * 'compound': (TopAbs_COMPOUND, topods_Compound)

        Parameters
        ----------
        shape: TopoDS_Shape
            the shape to cast
        shape_type: Union[str, TopAbs_SHAPE]
            the requested shape type

        Returns
        -------
        casted_shape: TopoDS_Shape
            The casted shape
        """

        if isinstance(shape_type, str):
            topabs_type, _ = SHAPE_TYPES[shape_type]
            return ExploreSubshapes.cast_shape(shape, topabs_type)

        rtn = {TopAbs_SOLID: topods.Solid,
               TopAbs_FACE: topods.Face,
               TopAbs_WIRE: topods.Wire,
               TopAbs_EDGE: topods.Edge,
               TopAbs_VERTEX: topods.Vertex,
               TopAbs_SHELL: topods.Shell,
               TopAbs_COMPOUND: topods.Compound,
               TopAbs_COMPSOLID: topods.CompSolid}

        if shape_type in rtn:
            return rtn[shape_type](shape)

        raise TypeError('Unkown type "{}"'.format(shape_type))

    @staticmethod
    def get_subshapes(shape: TopoDS_Shape, shape_type: Union[str, TopAbs_SHAPE]) -> Iterable[TopoDS_Shape]:
        """Return a container with the requested subshapes properly casted.

        Notes
        -----
        The dictonary is defined as follows:
            * 'vertex': (TopAbs_VERTEX, topods_Vertex),
            * 'edge': (TopAbs_EDGE, topods_Edge),
            * 'wire': (TopAbs_WIRE, topods_Wire),
            * 'face': (TopAbs_FACE, topods_Face),
            * 'shell': (TopAbs_SHELL, topods_Shell),
            * 'solid': (TopAbs_SOLID, topods_Solid),
            * 'compsolid': (TopAbs_COMPSOLID, topods_CompSolid),
            * 'compound': (TopAbs_COMPOUND, topods_Compound)

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to cast
        shape_type: Union[str, TopAbs_SHAPE]
            The requested shape types

        Returns
        -------
        subshapes: Iterable[types requested]
            The casted shapes
        """

        if isinstance(shape_type, str):
            topabs_type, _ = SHAPE_TYPES[shape_type]
            return ExploreSubshapes.get_subshapes(shape, topabs_type)

        subshape_map = TopTools_IndexedMapOfShape()
        topexp.MapShapes(shape, shape_type, subshape_map)
        subshapes = []
        for i in range(1, subshape_map.Size() + 1):
            subshapes.append(ExploreSubshapes.cast_shape(subshape_map(i), shape_type))

        return subshapes

    @staticmethod
    def get_solids(shape: TopoDS_Shape) -> Iterable[topods_Solid]:
        """Return a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopAbs_SOLID]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_SOLID)

    @staticmethod
    def get_faces(shape: TopoDS_Shape) -> Iterable[topods_Face]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopAbs_FACE]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_FACE)

    @staticmethod
    def get_wires(shape: TopoDS_Shape) -> Iterable[topods_Wire]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopAbs_WIRE]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_WIRE)

    @staticmethod
    def get_edges(shape: TopoDS_Shape) -> Iterable[topods_Edge]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        sh: TopoDS_Shape
            the shape to explore

        Returns
        -------
        s: Iterable[TopAbs_EDGE]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_EDGE)

    @staticmethod
    def get_vertices(shape: TopoDS_Shape) -> Iterable[topods_Vertex]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopAbs_VERTEX]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_VERTEX)

    @staticmethod
    def get_shells(shape: TopoDS_Shape) -> Iterable[topods_Shell]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopAbs_SHELL]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_SHELL)

    @staticmethod
    def get_compounds(shape: TopoDS_Shape) -> Iterable[topods_Compound]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopoDS_Compound]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_COMPOUND)

    @staticmethod
    def get_compsolids(shape: TopoDS_Shape) -> Iterable[topods_CompSolid]:
        """Returns a container with the requested subshapes properly casted.

        Parameters
        ----------
        shape: TopoDS_Shape
            The shape to explore

        Returns
        -------
        s: Iterable[TopAbs_COMPSOLID]
            The shapes of the type requested

        """
        return ExploreSubshapes.get_subshapes(shape, TopAbs_COMPSOLID)

    @staticmethod
    def edges_touching_shape(explored_shape: TopoDS_Shape,
                             ref_shape: Iterable[TopoDS_Shape],
                             tol: float = 1e-6) -> List[TopoDS_Edge]:
        """Return the edges of a shape in contact at end and start other shape.

        Parameters
        ----------
        explored_shape: TopoDS_Shape
            The shape containing the edges we want to extract
        ref_shape: Iterable[TopoDS_Shape]
            The reference shapes used to evaluate contact
        tol: float, optional
            Tolerance for contact. Default: 1e-6

        Returns
        -------
        touching_edges: List[TopoDS_Edges]
            The edges in contact

        """
        from pyoccad.create import CreateTopology
        from pyoccad.measure import shape

        touching_edges = []
        sae = ShapeAnalysis_Edge()
        for e in ExploreSubshapes.get_edges(explored_shape):
            d_lst = []
            for sh in ref_shape:
                my_sh_ref = CreateTopology.as_shape(sh)
                d1 = shape.distance(sae.FirstVertex(e), my_sh_ref)
                d2 = shape.distance(sae.LastVertex(e), my_sh_ref)
                d_lst += [d1, d2]
            if max(d_lst) < tol:
                touching_edges.append(e)
        return touching_edges
