from typing import Union, Sequence

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire
from OCC.Core.Geom import Geom_Surface, Geom_Curve
from OCC.Core.Precision import precision
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Face
from OCC.Core.gp import gp_Circ, gp_Elips

from pyoccad.create import CreateEdge, CreateBox
from pyoccad.typing import PointT


class CreateFace:
    """Factory to create faces.

    A face is a topology entity that describes a boundary unit of the 3D body.

    A face is described with its underlying surface and one or more wires.
    For instance a solid cylinder consists of 3 faces: bottom, top and lateral.

    Each of respective underlying surfaces is infinite (Geom_Plane and Geom_CylindricalSurface), while each face \
    bounds its surface with a wire:
        * two of them consist of a single edge lying on Geom_Circle and the lateral face consists of 4 edges
        * 2 are shared with top and bottom faces
        * and remaining two represent a seam edge, i.e. the face contains it twice in its wire (with different \
        orientations).

    For more information: https://opencascade.blogspot.com/2009/02/continued.html
    """

    @staticmethod
    def from_contour(contour: Union[Geom_Surface, TopoDS_Wire, TopoDS_Face, TopoDS_Edge, Geom_Curve, gp_Circ, gp_Elips],
                     tol_degenerated: float = precision.Confusion()) -> TopoDS_Face:
        """Build a face from a contour

        Parameters
        ----------
        contour: Union[Geom_Surface, TopoDS_Wire, TopoDS_Face, TopoDS_Edge, Geom_Curve, gp_Circ, gp_Elips]
            The contour of the face to build
        tol_degenerated: float, optional
            Tolerance value for resolution of degenerated edges {default=precision.Confusion()}

        Returns
        -------
        face: TopoDS_Face
            The resulting face
        """
        if isinstance(contour, Geom_Surface):
            return BRepBuilderAPI_MakeFace(contour, tol_degenerated).Face()
        if isinstance(contour, TopoDS_Wire):
            return BRepBuilderAPI_MakeFace(contour).Face()
        if isinstance(contour, TopoDS_Edge):
            return CreateFace.from_contour(BRepBuilderAPI_MakeWire(contour).Wire())
        if isinstance(contour, TopoDS_Face):
            return contour
        if isinstance(contour, (Geom_Curve, gp_Circ, gp_Elips)):
            return CreateFace.from_contour(CreateEdge.from_contour(contour))

        raise TypeError('Unhandled type "{}".'.format(type(contour)))

    @staticmethod
    def from_points(points: Sequence[PointT]):
        """Build a face from polygon. If not closed, the function will close the contour.

        Parameters
        ----------
        points: Sequence[PointT]
            The sequence of points

        Returns
        -------
        face: TopoDS_Face
            The resulting face
        """
        from pyoccad.create.curve.wire import CreateWire

        return CreateFace.from_contour(CreateWire.from_points(points, auto_close=True))

    @staticmethod
    def from_plane(pln):
        """Creates a plannar face centered on origin

        Parameters
        ----------
        pln : gp_Pln
            the face plane
        Returns
        -------
        f : TopoDS_Face
            the plannar face
        """
        return BRepBuilderAPI_MakeFace(pln).Face()

    @staticmethod
    def from_plane_and_sizes(pln, d1, d2):
        """Creates a plannar face centered on origin with given dimensions

        Parameters
        ----------
        pln : gp_Pln
            the face plane
        d1 : float
            Dimension in plane x direction
        d2 : float
            Dimension in plane y direction

        Returns
        -------
        f : TopoDS_Face
            the plannar face

        """
        return BRepBuilderAPI_MakeFace(pln, -d1 / 2, d1 / 2, -d2 / 2, d2 / 2).Face()

    @staticmethod
    def from_plane_and_shape_sizes(pln, sh):
        """Creates a plannar face inside shape's bounding box

        Parameters
        ----------
        pln : gp_Pln
            Plane used for face
        sh : TopoDS_Shape
            Shape used for bounding box

        Raises
        -------
        Exception

        Returns
        -------
        f : TopoDS_Face
            the resulting face

        """
        from pyoccad.transform import BooleanOperation
        from pyoccad.explore.subshapes import ExploreSubshapes

        d = precision.Infinite() / 10
        pln_face = CreateFace.from_plane_and_sizes(pln, d, d)
        box = CreateBox.bounding_box(sh)
        faces = ExploreSubshapes.get_faces(BooleanOperation.common([box], [pln_face]))
        if len(faces) == 0 or len(faces) > 1:
            raise Exception
        return faces[0]
