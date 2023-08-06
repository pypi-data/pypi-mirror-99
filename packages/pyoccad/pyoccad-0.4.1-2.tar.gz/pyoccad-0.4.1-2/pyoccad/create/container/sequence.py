from typing import Iterable, Union

from OCC.Core.TColGeom import TColGeom_SequenceOfCurve
from OCC.Core.Geom import Geom_Curve


class CreateSequence:
    """Factory to create an OpenCascade sequence."""

    @staticmethod
    def of_curves(curves: Iterable[Union[Geom_Curve, TColGeom_SequenceOfCurve]]) -> TColGeom_SequenceOfCurve:
        """Create an OpenCascade sequence of curves.

        Parameters
        ----------
        curves : iterable
            An iterable container of curves

        Returns
        -------
        sequence : TColGeom_SequenceOfCurve
        """
        sequence = TColGeom_SequenceOfCurve()
        for crv in curves:
            sequence.Append(crv)
        return sequence
