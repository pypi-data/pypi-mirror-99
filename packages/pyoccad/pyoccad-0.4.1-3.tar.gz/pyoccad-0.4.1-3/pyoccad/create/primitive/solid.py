from typing import Tuple, Union, Iterable

from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeSphere
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeHalfSpace
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.Geom import Geom_Surface, Geom_Curve
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Solid, TopoDS_Shape, TopoDS_Shell
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Pln

from pyoccad.create import CreatePoint, CreateDirection, CreateVector
from pyoccad.typing import PointT, VectorT


class CreateBox:

    @staticmethod
    def from_dimensions(dimensions: Tuple[float, float, float]) -> TopoDS_Solid:
        """Build a box with its first corner at (0., 0., 0.).

        Parameters
        ----------
        dimensions : Tuple[float, float, float]
            Dimension on x, y and z axis

        Returns
        -------
        box : TopoDS_Solid
            The resulting box
        """
        return BRepPrimAPI_MakeBox(*dimensions).Solid()

    @staticmethod
    def from_dimensions_and_center(dimensions: Tuple[float, float, float],
                                   center: PointT = (0, 0, 0)) -> TopoDS_Solid:
        """Build a box centered a a given point.

        Parameters
        ----------
        dimensions : Tuple[float, float, float]
            Dimension on x, y and z axis
        center : container of coordinates, optional
            Center of the box {default=(0., 0., 0.)}

        Returns
        -------
        box : TopoDS_Solid
            The resulting box
        """
        from pyoccad.transform import Translate
        from pyoccad.measure import solid

        box = BRepPrimAPI_MakeBox(*dimensions).Solid()
        cg = solid.center(box)
        vg = CreateVector.from_point(cg)
        vc = CreateVector.from_point(center)
        Translate.from_vector(box, vc - vg)

        return box

    Shape = Union[Adaptor3d_Curve, Geom_Curve, Geom_Surface, TopoDS_Shape]

    @staticmethod
    def bounding_box(shape: Union[Shape, Iterable[Shape]]):
        """Create a box containing a shape.

        Parameters
        ----------
        shape : Union[Shape, Iterable[Shape]]
            The shape

        Returns
        -------
        s : TopoDS_Solid
            The resulting box
        """
        from pyoccad.create import CreateTopology

        box = Bnd_Box()
        if not isinstance(shape, Iterable):
            shape = [shape]

        for sh in shape:
            brepbndlib.Add(CreateTopology.as_shape(sh), box)
        xmin, ymin, zmin, xmax, ymax, zmax = box.Get()

        return BRepPrimAPI_MakeBox(gp_Pnt(xmin, ymin, zmin), xmax - xmin, ymax - ymin, zmax - zmin).Solid()


class CreateCone:
    """Factory to build a cone."""

    @staticmethod
    def from_base_and_dir(base_center: PointT, vector: VectorT,
                          base_radius: float, top_radius: float = 0.) -> TopoDS_Solid:
        """Build a cone solid.

        Parameters
        ----------
        base_center : PointT
            The cone's origin
        vector : VectorT
            The vector representing the direction and height
        base_radius : float
            The base radius
        top_radius : float, optional
            The top radius {Default=0.}

        Returns
        -------
        cone : TopoDS_Solid
            The resulting cone
        """
        ax2 = gp_Ax2(CreatePoint.as_point(base_center), CreateDirection.as_direction(vector))
        return BRepPrimAPI_MakeCone(ax2, base_radius, top_radius, CreateVector.from_point(vector).Magnitude()).Solid()


class CreateSphere:
    """Factory to build a sphere."""

    @staticmethod
    def from_radius_and_center(radius: float, center: PointT = (0, 0, 0)) -> TopoDS_Solid:
        """Build a sphere solid.

        Parameters
        ----------
        radius : float
            The radius
        center : container of coordinates, optional
            The center {Default=(0, 0, 0)}

        Returns
        -------
        sphere : TopoDS_Solid
            The resulting sphere
        """
        return BRepPrimAPI_MakeSphere(CreatePoint.as_point(center), radius).Solid()


class CreateSolid:

    @staticmethod
    def from_shell(shell: TopoDS_Shell) -> TopoDS_Solid:
        """Build a solid from a shell.

        Parameters
        ----------
        shell: TopoDS_Shell
            The shell

        Returns
        -------
        solid : TopoDS_Solid
            The resulting solid
        """
        return BRepBuilderAPI_MakeSolid(shell).Solid()

    @staticmethod
    def half_space(plane: gp_Pln) -> TopoDS_Solid:
        """Build a half space solid, the outside part of the solid is toward plane's direction.

        Parameters
        ----------
        plane : gp_Pln
            The plane dividing space in 2 regions

        Returns
        -------
        solid : TopoDS_Solid
            The resulting half space
        """

        f = BRepBuilderAPI_MakeFace(plane).Face()
        p_in = plane.Location().Translated(CreateVector.from_point(plane.Axis().Direction()))
        return BRepPrimAPI_MakeHalfSpace(f, p_in).Solid()

    @staticmethod
    def half_space_from_face(face: TopoDS_Face, point: PointT) -> TopoDS_Solid:
        """Build half space from a face.

        Parameters
        ----------
        face : TopoDS_Face
            The face dividing space in 2 regions
        point : PointT
            A point to define which region is the half space

        Returns
        -------
        solid : TopoDS_Solid
            The resulting half space
        """
        return BRepPrimAPI_MakeHalfSpace(face, CreatePoint.as_point(point)).Solid()

    @staticmethod
    def half_space_from_surface(surface: Geom_Surface, point: PointT) -> TopoDS_Solid:
        """Build half space from a face.

        Parameters
        ----------
        surface : Geom_Surface
            The surface dividing space in 2 regions
        point : PointT
            A point to define which region is the half space

        Returns
        -------
        solid : TopoDS_Solid
            The resulting half space
        """
        face = BRepBuilderAPI_MakeFace(surface, 1e-6).Face()
        return CreateSolid.half_space_from_face(face, point)
