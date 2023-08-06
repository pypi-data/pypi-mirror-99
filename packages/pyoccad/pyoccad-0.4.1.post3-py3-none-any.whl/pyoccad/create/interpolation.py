from typing import Union, Sequence

from OCC.Core.Law import Law_Interpol
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_HArray1OfPnt2d

from pyoccad.create import CreateArray1


class CreateInterpolation:
    """Factory to create interpolations."""

    @staticmethod
    def of_points(container: Union[Sequence, TColgp_Array1OfPnt2d, TColgp_HArray1OfPnt2d]) -> Law_Interpol:
        """Creates a law from a list of values

        Notes
        -----
        A Law_Interpol provides an evolution law that interpolates a set of parameter and value pairs.

        Examples
        --------
        >>> # 1D Table definition
        >>> ParAndVal = [
        >>>    [0., 1.],
        >>>    [0.5 ,2.],
        >>>    [1., 3.]
        >>> ]
        >>> # Law definition
        >>> law_bs = law.interpolate(ParAndVal)
        >>> # Law evaluation
        >>> p = 0.75
        >>> v = law_bs(p)

        Parameters
        ----------
        container : Union[Sequence, TColgp_Array1OfPnt2d, TColgp_Array1OfPnt, TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt]
            A container of 2D or 3D points

        Returns
        -------
        law : Law_Interpol
        """
        if isinstance(container, (Sequence, TColgp_HArray1OfPnt2d)):
            container = CreateArray1.of_points(container)
        law = Law_Interpol()
        law.Set(container)
        return law
