from typing import Union

from OCC.Core.Geom import Geom_Geometry
from OCC.Core.Geom2d import Geom2d_Geometry
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Trsf, gp_Ax3, gp_Ax2, gp_Pln

from pyoccad.transform import Move
from pyoccad.typing import CoordSystem3T


class Rotate:
    """Factory to perform rotations."""

    @staticmethod
    def around_x(shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape],
                 angle: float,
                 inplace: bool = True,
                 axis: gp_Ax3 = gp_Ax3()) -> Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]:
        """Rotate around the x-axis of a geometrical reference or create a rotated copy of a shape.

        Parameters
        ----------
        shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape]
            The entity to move
        angle: float
            [rad] Angle
        inplace: bool, optional
            Whether to apply the transformation inplace {Default=True}
        axis: gp_Ax3, optional
            The geometrical reference {Default=Oxyz}

        Returns
        -------
        rotated_shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]
            Rotated shape if the transformation is not inplace, else None
        """
        from pyoccad.create import CreateRotation

        return Move.using_transformation(shape, CreateRotation.rotation_x(angle, axis), inplace)

    @staticmethod
    def around_y(shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape],
                 angle: float,
                 inplace: bool = True,
                 axis: gp_Ax3 = gp_Ax3()) -> Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]:
        """Rotate around the y-axis of a geometrical reference or create a rotated copy of a shape.

        Parameters
        ----------
        shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape]
            The entity to move
        angle: float
            [rad] Angle
        inplace: bool, optional
            Whether to apply the transformation inplace {Default=True}
        axis: gp_Ax3, optional
            The geometrical reference {Default=Oxyz}

        Returns
        -------
        rotated_shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]
            Rotated shape if the transformation is not inplace, else None
        """
        from pyoccad.create import CreateRotation

        return Move.using_transformation(shape, CreateRotation.rotation_y(angle, axis), inplace)

    @staticmethod
    def around_z(shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape],
                 angle: float,
                 inplace: bool = True,
                 axis: gp_Ax3 = gp_Ax3()) -> Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]:
        """Rotate around the z-axis of a geometrical reference or create a rotated copy of a shape.

        Parameters
        ----------
        shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape]
            The entity to move
        angle: float
            [rad] Angle
        inplace: bool, optional
            Whether to apply the transformation inplace {Default=True}
        axis: gp_Ax3, optional
            The geometrical reference {Default=Oxyz}

        Returns
        -------
        rotated_shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]
            Rotated shape if the transformation is not inplace, else None
        """
        from pyoccad.create import CreateRotation

        return Move.using_transformation(shape, CreateRotation.rotation_z(angle, axis), inplace)

    @staticmethod
    def between_coord_systems(shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape],
                              ax3_1: Union[CoordSystem3T, gp_Pln],
                              ax3_2: Union[CoordSystem3T, gp_Pln],
                              inplace: bool = True) -> Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]:
        """Move an entity from ax3_1 referential to ax3_2 referential

        Parameters
        ----------
        shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape]
            The shape
        ax3_1: Union[CoordSystem3T, gp_Pln]
            Initial referential
        ax3_2: Union[CoordSystem3T, gp_Pln]
            Final referential
        inplace: bool, optional
            Whether to apply the transformation inplace {Default=True}

        Returns
        -------
        rotated_shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]
            Rotated shape if the transformation is not inplace, else None
        """
        from pyoccad.create import CreateUnsignedCoordSystem

        transformation = gp_Trsf()

        def get_ax(ax):
            if isinstance(ax, (gp_Ax2, gp_Ax3)):
                return CreateUnsignedCoordSystem.as_coord_system(ax)
            if isinstance(ax3_1, gp_Pln):
                return ax.Position()
            raise TypeError('Type "{}" not handled.'.format(type(ax)))

        a_1 = get_ax(ax3_1)
        a_2 = get_ax(ax3_2)
        transformation.SetDisplacement(a_1, a_2)

        return Move.using_transformation(shape, transformation, inplace)
