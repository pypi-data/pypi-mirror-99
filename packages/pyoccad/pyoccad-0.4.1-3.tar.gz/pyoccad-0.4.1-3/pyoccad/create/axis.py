from typing import Union

from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax1, gp_Ax2d

from pyoccad.create import CreateDirection, CreatePoint
from pyoccad.typing import PointT, DirectionT, AxisT


class CreateAxis:
    """Factory to create axes.

    Notes
    -----
    An OpenCascade 'Ax1' describes an axis in 3D space.

    An axis is defined by:
        * its origin (also referred to as its "Location point")
    and
        * its unit vector (referred to as its "DirectionT" or "main DirectionT")

    An axis is used:
        * to describe 3D geometric entities (for example, the axis of a revolution entity). It serves the same purpose \
        as the STEP function "axis placement one axis"
    or
        * to define geometric transformations (axis of symmetry, axis of rotation, and so on). For example, \
        this entity can be used to locate a geometric entity or to define a symmetry axis
    """

    @staticmethod
    def as_axis(definition: AxisT) -> Union[gp_Ax1, gp_Ax2d]:
        """Create a 2D/3D axis from its definition.

        Parameters
        ----------
        definition: PointT
            The definition

        Returns
        -------
        axis: Union[gp_Ax1, gp_Ax2d]
            The resulting axis
        """

        if isinstance(definition, (gp_Ax1, gp_Ax2d)):
            return definition
        try:
            location, direction = definition
            return CreateAxis.from_location_and_direction(location, direction)
        except (ValueError, TypeError):
            pass

        raise TypeError('AxisT type not handled.')

    @staticmethod
    def ox() -> gp_Ax1:
        """Create an Ox axis.

        Returns
        -------
        axis: gp_Ax1
            The resulting axis
        """
        return gp_Ax1(gp_Pnt(), gp_Dir(1, 0, 0))

    @staticmethod
    def oy() -> gp_Ax1:
        """Create an Oy axis.

        Returns
        -------
        axis: gp_Ax1
            The resulting axis
        """
        return gp_Ax1(gp_Pnt(), gp_Dir(0, 1, 0))

    @staticmethod
    def oz() -> gp_Ax1:
        """Create an Oz axis.

        Returns
        -------
        axis: gp_Ax1
            The resulting axis
        """
        return gp_Ax1(gp_Pnt(), gp_Dir(0, 0, 1))

    @staticmethod
    def from_location_and_direction(location: PointT, direction: DirectionT) -> Union[gp_Ax1, gp_Ax2d]:
        """Create a 2D/3D axis from its location and direction.
    
        Parameters
        ----------
        location: PointT
            The location
        direction: DirectionT
            The direction
        
        Returns 
        -------
        axis: Union[gp_Ax1, gp_Ax2d]
            The resulting axis
        """
        from pyoccad.measure.direction import MeasureDirection
        from pyoccad.measure.point import MeasurePoint

        location_ = CreatePoint.as_point(location)
        direction_ = CreateDirection.as_direction(direction)

        location_dim = MeasurePoint.dimension(location_)
        direction_dim = MeasureDirection.dimension(direction_)
        if location_dim != direction_dim:
            raise TypeError('AxisT position and direction should both have the same dimension '
                            'which is either 2 or 3, got {} and {}.'.format(location_dim, direction_dim))

        if location_dim == 2:
            axis = gp_Ax2d(location_, direction_)
        else:
            axis = gp_Ax1(location_, direction_)

        return axis
