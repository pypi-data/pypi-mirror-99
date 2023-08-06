from typing import Union, List, Tuple

import numpy as np
from OCC.Core.gp import gp_Vec, gp_Vec2d, gp_Pnt, gp_Pnt2d, gp_XY, gp_XYZ, gp_Dir, gp_Dir2d

from pyoccad.create.direction import CreateDirection
from pyoccad.typing import VectorT, DirectionT, PointT


class CreateVector:
    """Factory to create vectors."""

    @staticmethod
    def as_vector(definition: VectorT) -> Union[gp_Vec, gp_Vec2d]:
        """Create a 2D/3D vector.

        Parameters
        ----------
        definition: VectorT
            The vector definition

        Returns
        -------
        vector: Union[gp_Vec, gp_Vec2d]
            The resulting vector
        """
        from pyoccad.create.point import CreatePoint

        if isinstance(definition, (gp_Vec, gp_Vec2d)):
            return definition

        if isinstance(definition, (gp_Pnt, gp_XYZ, gp_Dir)):
            return gp_Vec(*definition.Coord())

        if isinstance(definition, (gp_Pnt2d, gp_XY, gp_Dir2d)):
            return gp_Vec2d(*definition.Coord())

        try:  # assume a vector defined with only its ending point
            return CreateVector.as_vector(CreatePoint.as_point(definition))
        except TypeError:
            pass

        try:  # assume a vector defined with two points
            point1, point2 = [CreatePoint.as_point(v) for v in definition]
            return CreateVector.from_2_points(point1, point2)
        except (ValueError, TypeError):
            pass

        try:  # assume a vector defined with its direction and norm
            direction, norm = definition
            return CreateVector.from_direction_norm(direction, norm)
        except (ValueError, TypeError):
            pass

        raise TypeError('VectorT type not handled.')

    @staticmethod
    def as_list(vector: VectorT) -> List[float]:
        """Create a vector as a Python list.

        Parameters
        ----------
        vector: VectorT
            The vector

        Returns
        -------
        list: List[float]
            The resulting vector formatted as a Python list
        """

        return [*CreateVector.as_tuple(vector)]

    @staticmethod
    def as_tuple(vector: VectorT) -> Union[Tuple[float, float], Tuple[float, float, float]]:
        """Create a vector as a Python tuple.

        Parameters
        ----------
        vector: VectorT
            The vector

        Returns
        -------
        tuple: Union[Tuple[float, float], Tuple[float, float, float]]
            The resulting vector formatted as a Python tuple
        """

        return CreateVector.as_vector(vector).Coord()

    @staticmethod
    def as_ndarray(vector: VectorT) -> np.ndarray:
        """Create a vector as a Numpy array.

        Parameters
        ----------
        vector: VectorT
            The vector

        Returns
        -------
        array: np.ndarray[float]
            The resulting vector formatted as a Numpy array
        """

        return np.array(CreateVector.as_tuple(vector))

    @staticmethod
    def from_point(point: PointT) -> Union[gp_Vec, gp_Vec2d]:
        """Create a 2D/3D vector from a point.

        It assumes the starting point is the center of the referential, the ending point is the provided point.

        Parameters
        ----------
        point: PointT
            The vector ending point

        Returns
        -------
        vector: Union[gp_Vec, gp_Vec2d]
            The resulting vector
        """
        return CreateVector.as_vector(point)

    @staticmethod
    def from_2_points(starting_point: PointT, ending_point: PointT) -> Union[gp_Vec, gp_Vec2d]:
        """Create a 2D/3D vector from two points.

        Parameters
        ----------
        starting_point: PointT
            The starting point
        ending_point: PointT
            The ending point

        Returns
        -------
        vector: Union[gp_Vec, gp_Vec2d]
            The resulting vector
        """
        from pyoccad.create.point import CreatePoint
        from pyoccad.measure.point import MeasurePoint

        point1 = CreatePoint.as_point(starting_point)
        point2 = CreatePoint.as_point(ending_point)
        dimension = MeasurePoint.unique_dimension((point1, point2))

        if dimension == 3:
            vector_ = gp_Vec(point1, point2)
        else:  # dimension == 2
            vector_ = gp_Vec2d(point1, point2)

        return vector_

    @staticmethod
    def from_direction_norm(direction: DirectionT, norm: float) -> Union[gp_Vec, gp_Vec2d]:
        """Create a vector from a direction and a norm.

        Parameters
        ----------
        direction : {coordinates container}
            The direction of the vector
        norm : float
            The vector magnitude/norm

        Returns
        -------
        vector: Union[gp_Vec, gp_Vec2d]
            The resulting vector
        """
        from pyoccad.create.point import CreatePoint

        return CreateVector.as_vector(CreatePoint.as_point(CreateDirection.as_ndarray(direction) * norm))

    @staticmethod
    def from_direction_relative_tension(direction: DirectionT,
                                        tension: float,
                                        reference: float) -> Union[gp_Vec, gp_Vec2d]:
        """Create a vector from a direction and a norm computed with a relative tension and a reference distance.

        Parameters
        ----------
        direction: DirectionT
            The direction of the vector
        tension : float
            The vector magnitude/norm as a percentage of the reference distance
        reference : float
            The reference distance

        Returns
        -------
        vector: Union[gp_Vec, gp_Vec2d]
            The resulting vector
        """

        return CreateVector.from_point(CreateDirection.as_ndarray(direction) * tension * reference)

    @staticmethod
    def x_vec() -> gp_Vec:
        """Create a unit vector oriented by the x-axis."""
        return gp_Vec(1, 0, 0)

    @staticmethod
    def y_vec() -> gp_Vec:
        """Create a unit vector oriented by the y-axis."""
        return gp_Vec(0, 1, 0)

    @staticmethod
    def z_vec() -> gp_Vec:
        """Create a unit vector oriented by the z-axis."""
        return gp_Vec(0, 0, 1)

    @staticmethod
    def ox() -> gp_Vec:
        """Create a unit vector oriented by the x-axis."""
        return CreateVector.x_vec()

    @staticmethod
    def oy() -> gp_Vec:
        """Create a unit vector oriented by the y-axis."""
        return CreateVector.y_vec()

    @staticmethod
    def oz() -> gp_Vec:
        """Create a unit vector oriented by the z-axis."""
        return CreateVector.z_vec()
