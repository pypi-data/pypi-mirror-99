from typing import Union

from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Dir, gp_Dir2d, gp_Ax2, gp_Ax3, gp_Ax22d

from pyoccad.create import CreateAxis, CreateDirection, CreatePoint
from pyoccad.typing import PointT, DirectionT, CoordSystemT


class CreateCoordSystem:
    """Factory to create coordinate systems.

    An OpenCascade 'Ax2' describes a right-handed, coordinate system in 3D space.

    A coordinate system is defined by:
        * its origin (also referred to as its "Location point"), and

        * three orthogonal unit vectors, termed respectively the "X Direction", the "Y Direction" and the \
        "Direction" (also referred to as the "main Direction").

    The "Direction" of the coordinate system is called its "main Direction" because whenever this unit vector is
    modified, the "X Direction" and the "Y Direction" are recomputed.

    However, when we modify either the "X Direction" or the "Y Direction", "Direction" is not modified. The "main
    Direction" is also the "Z Direction".

    Since an Ax2 coordinate system is right-handed, its "main Direction" is always equal to the cross product of
    its "X Direction" and "Y Direction". (To define a left-handed coordinate system, use gp_Ax3.)

    A coordinate system is used:
        * to describe geometric entities, in particular to position them. The local coordinate system of a \
        geometric entity serves the same purpose as the STEP function "axis placement two axes"

    OR
        * to define geometric transformations.

    Note: we refer to the "X Axis", "Y Axis" and "Z Axis", respectively, as to axes having:
        * the origin of the coordinate system as their origin

    AND
        * the unit vectors "X Direction", "Y Direction" and "main Direction", respectively, as their unit vectors. \
        The "Z Axis" is also the "main Axis".
    """

    @staticmethod
    def as_coord_system(definition: CoordSystemT) -> Union[gp_Ax2, gp_Ax22d]:
        """Create a coordinate system from its definition.

        Parameters
        ----------
        definition: CoordSystemT
            The definition

        Returns
        -------
        axis: Union[gp_Ax2, gp_Ax22d]
            The resulting axis
        """

        if isinstance(definition, (gp_Ax2, gp_Ax22d)):
            return definition

        if isinstance(definition, gp_Ax3):
            return CreateCoordSystem.from_location_and_directions(definition.Location(),
                                                                  definition.XDirection(),
                                                                  definition.Direction())

        try:
            location, x_direction, n_direction = definition
            return CreateCoordSystem.from_location_and_directions(location, x_direction, n_direction)
        except (ValueError, TypeError):
            pass

        raise TypeError('Coordinate system type not handled.')

    @staticmethod
    def ox() -> gp_Ax2:
        """Create a coordinate system oriented by the Ox direction.

        Returns
        -------
        coord_system: gp_Ax2
            The resulting system coordinate
        """
        ax2 = gp_Ax2()
        ax2.SetAxis(CreateAxis.ox())
        return ax2

    @staticmethod
    def oy() -> gp_Ax2:
        """Create a coordinate system oriented by the Oy direction.

        Returns
        -------
        coord_system: gp_Ax2
            The resulting system coordinate
        """
        ax2 = gp_Ax2()
        ax2.SetAxis(CreateAxis.oy())
        return ax2

    @staticmethod
    def oz() -> gp_Ax2:
        """Create a coordinate system oriented by the Oz direction.

        Returns
        -------
        coord_system: gp_Ax2
            The resulting system coordinate
        """
        ax2 = gp_Ax2()
        ax2.SetAxis(CreateAxis.oz())
        return ax2

    @staticmethod
    def rotated_ox(angle: float) -> gp_Ax2:
        """Create a coordinate system oriented by the Ox direction, rotated by a given angle.

        Parameters
        ----------
        angle: float
            [rad] The rotation angle

        Returns
        -------
        coord_system: gp_Ax2
            The resulting system coordinate
        """
        ax2 = gp_Ax2()
        ax2.SetAxis(CreateAxis.ox())
        ax2.Rotate(ax2.Axis(), angle)
        return ax2

    @staticmethod
    def rotated_oy(angle: float) -> gp_Ax2:
        """Create a coordinate system oriented by the Oy direction, rotated by a given angle.

        Parameters
        ----------
        angle: float
            [rad] The rotation angle

        Returns
        -------
        coord_system: gp_Ax2
            The resulting system coordinate
        """
        ax2 = gp_Ax2()
        ax2.SetAxis(CreateAxis.oy())
        ax2.Rotate(ax2.Axis(), angle)
        return ax2

    @staticmethod
    def rotated_oz(angle: float) -> gp_Ax2:
        """Create a coordinate system oriented by the Oz direction, rotated by a given angle.

        Parameters
        ----------
        angle: float
            [rad] The rotation angle

        Returns
        -------
        coord_system: gp_Ax2
            The resulting system coordinate
        """
        ax2 = gp_Ax2()
        ax2.SetAxis(CreateAxis.oz())
        ax2.Rotate(ax2.Axis(), angle)
        return ax2

    @staticmethod
    def from_location_and_directions(location: PointT,
                                     x_direction: DirectionT,
                                     direction: DirectionT) -> Union[gp_Ax2, gp_Ax22d]:
        """Create a 3D right-handed coordinate system.

        Parameters
        ----------
        location: PointT
            The location/origin
        x_direction: DirectionT
            The x-axis direction
        direction: DirectionT
            The z-axis direction when 3D coordinate system, y-axis when 2D

        Returns
        -------
        coord_system: Union[gp_Ax2, gp_Ax22d]
            The resulting coordinate system
        """
        from pyoccad.measure import MeasurePoint, MeasureDirection

        loc = CreatePoint.as_point(location)
        direction = CreateDirection.as_direction(direction)
        dx = CreateDirection.as_direction(x_direction)

        if isinstance(loc, gp_Pnt2d) and isinstance(direction, gp_Dir2d) and isinstance(dx, gp_Dir2d):
            return gp_Ax22d(loc, dx, direction)
        if isinstance(loc, gp_Pnt) and isinstance(direction, gp_Dir) and isinstance(dx, gp_Dir):
            return gp_Ax2(loc, direction, dx)

        raise TypeError('Location and directions should all have the same dimension '
                        'which is either 2 or 3, got {}, {} and {}.'.format(MeasurePoint.dimension(loc),
                                                                            MeasureDirection.dimension(direction),
                                                                            MeasureDirection.dimension(dx)))


class CreateUnsignedCoordSystem:
    """Factory to create unsigned coordinate systems.

    Notes
    -----
    An OpenCascade 'Ax3' describes a coordinate system in 3D space.

    Unlike a gp_Ax2 coordinate system, a gp_Ax3 can be right-handed ('direct sense') or
    left-handed ('indirect sense').
    """

    @staticmethod
    def as_coord_system(definition: CoordSystemT) -> gp_Ax3:
        """Create a coordinate system from its definition.

        Parameters
        ----------
        definition: CoordSystemT
            The definition

        Returns
        -------
        axis: gp_Ax3
            The resulting axis
        """

        if isinstance(definition, gp_Ax3):
            return definition

        if isinstance(definition, gp_Ax2):
            return gp_Ax3(definition)

        try:
            location, x_direction, n_direction = definition
            return CreateUnsignedCoordSystem.from_location_and_directions(location, x_direction, n_direction)
        except (ValueError, TypeError):
            pass

        raise TypeError('Coordinate system type not handled.')

    @staticmethod
    def ox() -> gp_Ax3:
        """Create a coordinate system oriented by the Ox direction.

        Returns
        -------
        coord_system: gp_Ax3
            The resulting system coordinate
        """
        return gp_Ax3(CreateCoordSystem.ox())

    @staticmethod
    def oy() -> gp_Ax3:
        """Create a coordinate system oriented by the Oy direction.

        Returns
        -------
        coord_system: gp_Ax3
            The resulting system coordinate
        """
        return gp_Ax3(CreateCoordSystem.oy())

    @staticmethod
    def oz() -> gp_Ax3:
        """Create a coordinate system oriented by the Oz direction.

        Returns
        -------
        coord_system: gp_Ax3
            The resulting system coordinate
        """
        return gp_Ax3(CreateCoordSystem.oz())

    @staticmethod
    def from_location_and_directions(location: PointT,
                                     x_direction: DirectionT,
                                     direction: DirectionT) -> gp_Ax3:
        """Create a 3D right-handed coordinate system.
    
        Parameters
        ----------
        location: PointT
            The location/origin
        x_direction: DirectionT
            The x-axis direction
        direction: DirectionT
            The z-axis direction

        Returns 
        -------
        coord_system: gp_Ax3
            The resulting coordinate system
        """
        loc = CreatePoint.as_point(location)
        dn = CreateDirection.as_direction(direction)
        dx = CreateDirection.as_direction(x_direction)

        return gp_Ax3(loc, dn, dx)
