from typing import Iterable

from OCC.Core.gp import gp_Pnt

from pyoccad.typing import PointT


class MeasurePoint:
    """Factory to measure points."""

    @staticmethod
    def dimension(point: PointT) -> int:
        """Get the dimension of a point.

        Parameters
        ----------
        point : PointT
            The point

        Returns
        -------
        dimension : int
            The dimension of the point (2 or 3)
        """
        from pyoccad.create import CreatePoint

        if isinstance(CreatePoint.as_point(point), gp_Pnt):
            return 3
        return 2

    @staticmethod
    def unique_dimension(points: Iterable[PointT]) -> int:
        dimensions = [MeasurePoint.dimension(point) for point in points]
        if len(set(dimensions)) > 1:
            raise TypeError('Points should all have the same dimension, got dimensions {}.'.format(dimensions))

        return dimensions[0]
