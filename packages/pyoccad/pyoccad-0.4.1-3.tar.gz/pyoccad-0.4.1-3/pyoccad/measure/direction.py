from OCC.Core.gp import gp_Dir

from pyoccad.typing import DirectionT


class MeasureDirection:
    """Factory to measure a direction."""

    @staticmethod
    def dimension(direction: DirectionT) -> int:
        """Get the dimension of a direction.

        Parameters
        ----------
        direction : DirectionT
            The direction

        Returns
        -------
        dimension : int
            The dimension of the direction (2 or 3)
        """
        from pyoccad.create import CreateDirection

        if isinstance(CreateDirection.as_direction(direction), gp_Dir):
            return 3
        return 2
