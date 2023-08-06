from OCC.Core.gp import gp_Ax1

from pyoccad.typing import AxisT


class MeasureAxis:
    """Factory to measure an axis."""

    @staticmethod
    def dimension(axis: AxisT) -> int:
        """Get the dimension of an axis.

        Parameters
        ----------
        axis : AxisT
            The axis

        Returns
        -------
        dimension : int
            The dimension of the axis (2 or 3)
        """
        from pyoccad.create import CreateAxis

        axis_ = CreateAxis.as_axis(axis)
        if isinstance(axis_, gp_Ax1):
            return 3
        return 2
