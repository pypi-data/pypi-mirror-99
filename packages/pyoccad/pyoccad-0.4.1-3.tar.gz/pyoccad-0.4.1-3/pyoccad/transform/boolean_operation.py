from typing import Union, Iterable, Sequence

from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Splitter, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, \
    BRepAlgoAPI_Section
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeHalfSpace
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import topods, TopoDS_Shape, TopoDS_Wire, TopoDS_Edge
from OCC.Core.gp import gp_Trsf, gp_Pln, gp_Circ, gp_Elips

from pyoccad.typing import DirectionT


class BooleanOperation:

    @staticmethod
    def common(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
               tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]) -> TopoDS_Shape:
        """Create a common boolean operation.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Main shapes
        tools : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Tool shapes

        Returns
        -------
        common_shape: TopoDS_Shape
            The resulting common shape
        """
        from pyoccad.create import CreateOCCList

        common_ = BRepAlgoAPI_Common()
        args_lst = CreateOCCList.of_shapes(shapes)
        tools_lst = CreateOCCList.of_shapes(tools)
        common_.SetTools(tools_lst)
        common_.SetArguments(args_lst)
        common_.SetRunParallel(True)
        common_.Build()
        return common_.Shape().Moved(TopLoc_Location(gp_Trsf()))  # Needs to build a copy, if not the shape is deleted

    @staticmethod
    def split(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
              tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]) -> TopoDS_Shape:
        """Create a split boolean operation.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Main shapes
        tools : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Tool shapes

        Returns
        -------
        split_shape : TopoDS_Shape
            The resulting split shape
        """
        from pyoccad.create import CreateOCCList

        split_ = BRepAlgoAPI_Splitter()
        args_lst = CreateOCCList.of_shapes(shapes)
        tools_lst = CreateOCCList.of_shapes(tools)
        split_.SetTools(tools_lst)
        split_.SetArguments(args_lst)
        split_.SetRunParallel(True)
        split_.Build()
        return split_.Shape().Moved(TopLoc_Location(gp_Trsf()))  # Needs to build a copy, if not the shape is deleted

    @staticmethod
    def cut(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
            tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]) -> TopoDS_Shape:
        """Create a cut boolean operation.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Main shapes
        tools : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Tool shapes

        Returns
        -------
        cut_shape : TopoDS_Shape
            The resulting cut shape
        """
        from pyoccad.create import CreateOCCList

        cut_ = BRepAlgoAPI_Cut()
        args_lst = CreateOCCList.of_shapes(shapes)
        tools_lst = CreateOCCList.of_shapes(tools)
        cut_.SetTools(tools_lst)
        cut_.SetArguments(args_lst)
        cut_.SetRunParallel(True)
        cut_.Build()
        return cut_.Shape().Moved(TopLoc_Location(gp_Trsf()))  # Needs to build a copy, if not the shape is deleted

    @staticmethod
    def cut_half_space(shapes: Iterable[TopoDS_Shape], plane: gp_Pln, normale_side: bool = True) -> TopoDS_Shape:
        """Cut shapes with half space.

        Parameters
        ----------
        shapes : Iterable[TopoDS_Shape]
            Shapes to cut
        plane : gp_Pln
            The cut plane
        normale_side: bool
            Whether the plane's normal is included in the half space {Default=True}

        Returns
        -------
        cut_shape : TopoDS_Shape
            The resulting cut shape
        """
        from pyoccad.create import CreateVector

        fa = BRepBuilderAPI_MakeFace(plane).Face()
        if normale_side:
            d = 1.
        else:
            d = -1.
        p = plane.Location().Translated(CreateVector.from_point(plane.Axis().Direction()) * d)
        hs = BRepPrimAPI_MakeHalfSpace(fa, p).Solid()
        return BooleanOperation.cut(shapes, [hs])

    @staticmethod
    def extrude_cut(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
                    contour: Union[Geom_Surface, TopoDS_Wire, TopoDS_Edge, Geom_Curve, gp_Circ, gp_Elips],
                    direction: DirectionT) -> TopoDS_Shape:
        """Cut then extrude along a direction.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Shapes to cut
        contour : Union[Geom_Surface, TopoDS_Wire, TopoDS_Edge, Geom_Curve, gp_Circ, gp_Elips]
            A closed contour used for cut
        direction : DirectionT
            Extrusion direction

        Returns
        -------
        cut_shape : TopoDS_Shape
            The resulting cut shape
        """
        from pyoccad.create import CreateVector, CreatePoint, CreateBox, CreateExtrusion
        from pyoccad.measure import shape

        d_extr = CreatePoint.as_point(direction)
        vec = CreateVector.from_point(d_extr).Scaled(1.2 * shape.encompassing_sphere_diameter(shapes + [contour]))
        extr = CreateExtrusion.surface(contour, vec, is_infinite=False, half_infinite=True)
        extr = BooleanOperation.common([extr], [CreateBox.bounding_box(shapes)])
        return BooleanOperation.cut(shapes, [extr])

    @staticmethod
    def __fuse_builder(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
                       tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
                       ) -> BRepAlgoAPI_Fuse:
        """Create a fuse boolean operation.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Main shapes
        tools : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Tool shapes

        Returns
        -------
        fuse_builder : BRepAlgoAPI_Fuse
            The fuse builder
        """
        from pyoccad.create import CreateOCCList

        fuse_ = BRepAlgoAPI_Fuse()
        args_lst = CreateOCCList.of_shapes(shapes)
        tools_lst = CreateOCCList.of_shapes(tools)
        fuse_.SetTools(tools_lst)
        fuse_.SetArguments(args_lst)
        fuse_.SetRunParallel(True)
        fuse_.Build()
        return fuse_

    @staticmethod
    def fuse(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
             tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
             ) -> TopoDS_Shape:
        """Create a fuse boolean operation.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Main shapes
        tools : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            Tool shapes

        Returns
        -------
        fused_shape : TopoDS_Shape
            The resulting fused shape
        """
        # Needs to build a copy, if not the shape is deleted
        builder = BooleanOperation.__fuse_builder(shapes, tools)
        return builder.Shape().Moved(TopLoc_Location(gp_Trsf()))

    @staticmethod
    def fuse_with_fillet(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
                         tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
                         radius: float) -> TopoDS_Shape:
        """Create a fuse boolean operation, then build a fillet.

        Parameters
        ----------
        shapes : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            List of principal shapes
        tools : Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]]
            List of tool shapes
        radius : float
            Fillet value

        Returns
        -------
        shape : TopoDS_Shape
            The resulting fused with fillet shape
        """
        from pyoccad.create import CreateList

        fuse_ = BooleanOperation.__fuse_builder(shapes, tools)
        fillet_builder = BRepFilletAPI_MakeFillet(fuse_.Shape())
        for e in CreateList.from_occ_list(fuse_.SectionEdges()):
            fillet_builder.Add(radius, topods.Edge(e))
        return fillet_builder.Shape()

    @staticmethod
    def section(shapes: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
                tools: Iterable[Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]],
                use_approximation: bool = False) -> TopoDS_Shape:
        """Create the intersection between shapes.

        Parameters
        ----------
        shapes : {container of Adaptor3d_Curve, Geom_curve, Geom_Surface, TopoDS_Shape}
            List of principal shapes
        tools : {container of Adaptor3d_Curve, Geom_curve, Geom_Surface, TopoDS_Shape}
            List of tool shapes
        use_approximation : bool, optional
            Whether to use of approximation (this can speed up the computations made on result) {Default=False}

        Returns
        -------
        section_shape : TopoDS_Shape
            The resulting section shape
        """
        from pyoccad.create import CreateOCCList

        section_ = BRepAlgoAPI_Section()
        args_lst = CreateOCCList.of_shapes(shapes)
        tools_lst = CreateOCCList.of_shapes(tools)
        section_.SetTools(tools_lst)
        section_.SetArguments(args_lst)
        section_.SetRunParallel(True)
        section_.Approximation(use_approximation)
        section_.Build()
        return section_.Shape().Moved(
            TopLoc_Location(gp_Trsf()))  # Needs to build a copy, if not the shape is deleted
