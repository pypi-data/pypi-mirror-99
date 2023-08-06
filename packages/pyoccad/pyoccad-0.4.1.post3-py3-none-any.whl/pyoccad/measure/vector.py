from OCC.Core.gp import gp_Vec

from pyoccad.typing import VectorT


class MeasureVector:
    """Factory to measure vectors."""

    @staticmethod
    def dimension(definition: VectorT) -> int:
        """Measure the dimension of a vector.

        Parameters
        ----------
        definition: VectorT
            The definition

        Returns
        -------
        dimension: int
            The dimension of the vector (2 or 3)
        """
        from pyoccad.create import CreateVector

        vector = CreateVector.as_vector(definition)
        if isinstance(vector, gp_Vec):
            return 3
        return 2
