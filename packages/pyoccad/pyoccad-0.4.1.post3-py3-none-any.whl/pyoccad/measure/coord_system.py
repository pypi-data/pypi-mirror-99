from OCC.Core.gp import gp_Ax2

from pyoccad.typing import CoordSystemT


class MeasureCoordSystem:
    """Factory to measure a coordinate system."""

    @staticmethod
    def dimension(coord_system: CoordSystemT) -> int:
        """Get the dimension of a coordinate system.

        Parameters
        ----------
        coord_system: CoordSystemT
            The coordinate system

        Returns
        -------
        dimension : int
            The dimension of the coordinate system (2 or 3)
        """
        from pyoccad.create import CreateCoordSystem

        coord_system_ = CreateCoordSystem.as_coord_system(coord_system)
        if isinstance(coord_system_, gp_Ax2):
            return 3
        return 2
