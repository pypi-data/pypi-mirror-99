from math import radians
from typing import Union, List, Tuple

import numpy as np
from OCC.Core.gp import gp_Dir, gp_Dir2d, gp_Pnt, gp_Pnt2d, gp_Vec, gp_Vec2d, gp_XYZ, gp_XY

from pyoccad.typing import DirectionT


class CreateDirection:
    """Factory to create directions.

    Notes
    -----
    A direction is a unit vector in 2D or 3D space.
    """
    @staticmethod
    def as_direction(direction: DirectionT) -> Union[gp_Dir, gp_Dir2d]:
        """Create a 2D/3D direction.

        Parameters
        ----------
        direction: DirectionT
            The direction

        Returns
        -------
        dir : Union[gp_Dir, gp_Dir2d]
            The direction
        """
        if isinstance(direction, (gp_Dir, gp_Dir2d)):
            return direction

        if isinstance(direction, (gp_Pnt, gp_Vec, gp_XYZ)):
            return gp_Dir(*direction.Coord())

        if isinstance(direction, (gp_Pnt2d, gp_Vec2d, gp_XY)):
            return gp_Dir2d(*direction.Coord())

        if isinstance(direction, np.ndarray):
            dimension = direction.size
            if not (2 <= dimension <= 3 and direction.ndim == 1):
                raise TypeError('PointT should have dimension 2 or 3, got {}.'.format(dimension))
            direction = direction.tolist()

        if isinstance(direction, (tuple, list)):
            dimension = len(direction)
            types = [type(element) for element in direction]
            unique_types = set(types)

            if unique_types.issubset({float, int, np.float_, np.int_}):
                if dimension == 3:
                    return gp_Dir(*direction)
                if dimension == 2:
                    return gp_Dir2d(*direction)
                raise TypeError('Exactly 2 or 3 coordinates expected to define a direction, '
                                'got {}.'.format(dimension))

            raise TypeError('DirectionT coordinates have unsupported type(s): should be int or float, '
                            'got {}.'.format(unique_types))

        raise TypeError('DirectionT type not handled.')

    @staticmethod
    def as_tuple(direction: DirectionT) -> Union[Tuple[float, float], Tuple[float, float, float]]:
        """Create a 2D/3D direction.

        Parameters
        ----------
        direction: DirectionT
            The direction

        Returns
        -------
        dir : Union[Tuple[float, float], Tuple[float, float, float]]
            The direction
        """
        return CreateDirection.as_direction(direction).Coord()

    @staticmethod
    def as_list(direction: DirectionT) -> List[float]:
        """Create a 2D/3D direction.

        Parameters
        ----------
        direction: DirectionT
            The direction

        Returns
        -------
        dir : List[float]
            The direction
        """
        return [*CreateDirection.as_tuple(direction)]

    @staticmethod
    def as_ndarray(direction: DirectionT) -> np.ndarray:
        """Create a 2D/3D direction.

        Parameters
        ----------
        direction: DirectionT
            The direction

        Returns
        -------
        dir : np.ndarray
            The direction
        """
        return np.array(CreateDirection.as_tuple(direction))

    @staticmethod
    def in_xy_plane(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the xy plane.

        Parameters
        ----------
        angle : float
            [rad] The angle

        Returns
        -------
        dir : gp_Dir
            The direction
        """
        from pyoccad.create.axis import CreateAxis

        return CreateDirection.x_dir().Rotated(CreateAxis.oz(), angle)

    @staticmethod
    def in_xz_plane(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the xz plane.

        Parameters
        ----------
        angle : float
            [rad] The angle

        Returns
        -------
        dir : gp_Dir
            The direction
        """
        from pyoccad.create.axis import CreateAxis

        return CreateDirection.x_dir().Rotated(CreateAxis.oy(), angle)

    @staticmethod
    def in_zx_plane(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the zx plane.

         Parameters
         ----------
         angle : float
             [rad] The angle

         Returns
         -------
         dir : gp_Dir
             The direction
         """
        from pyoccad.create.axis import CreateAxis

        return CreateDirection.z_dir().Rotated(CreateAxis.oy(), angle)

    @staticmethod
    def in_zy_plane(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the zy plane.

         Parameters
         ----------
         angle : float
             [rad] The angle

         Returns
         -------
         dir : gp_Dir
             The direction
         """
        from pyoccad.create.axis import CreateAxis

        return CreateDirection.z_dir().Rotated(CreateAxis.ox(), angle)

    @staticmethod
    def in_xy_plane_deg(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the xy plane.

        Parameters
        ----------
        angle : float
            [deg] The angle

        Returns
        -------
        dir : gp_Dir
            The direction
        """
        return CreateDirection.in_xy_plane(radians(angle))

    @staticmethod
    def in_xz_plane_deg(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the xz plane.

        Parameters
        ----------
        angle : float
            [deg] The angle

        Returns
        -------
        dir : gp_Dir
            The direction
        """
        return CreateDirection.in_xz_plane(radians(angle))

    @staticmethod
    def in_zx_plane_deg(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the zx plane.

         Parameters
         ----------
         angle : float
             [deg] The angle

         Returns
         -------
         dir : gp_Dir
             The direction
         """
        return CreateDirection.in_zx_plane(radians(angle))

    @staticmethod
    def in_zy_plane_deg(angle: float) -> gp_Dir:
        """Create a direction oriented by an angle in the zy plane.

         Parameters
         ----------
         angle : float
             [deg] The angle

         Returns
         -------
         dir : gp_Dir
             The direction
         """
        return CreateDirection.in_zy_plane(radians(angle))

    @staticmethod
    def x_dir() -> gp_Dir:
        """Create a direction oriented by the x-axis."""
        return gp_Dir(1, 0, 0)

    @staticmethod
    def y_dir() -> gp_Dir:
        """Create a direction oriented by the y-axis."""
        return gp_Dir(0, 1, 0)

    @staticmethod
    def z_dir() -> gp_Dir:
        """Create a direction oriented by the z-axis."""
        return gp_Dir(0, 0, 1)

    @staticmethod
    def ox() -> gp_Dir:
        """Create a direction oriented by the x-axis."""
        return CreateDirection.x_dir()

    @staticmethod
    def oy() -> gp_Dir:
        """Create a direction oriented by the y-axis."""
        return CreateDirection.y_dir()

    @staticmethod
    def oz() -> gp_Dir:
        """Create a direction oriented by the z-axis."""
        return CreateDirection.z_dir()
