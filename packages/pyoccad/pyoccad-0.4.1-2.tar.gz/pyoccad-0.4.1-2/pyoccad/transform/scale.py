from typing import Union

from OCC.Core.Geom import Geom_Geometry
from OCC.Core.Geom2d import Geom2d_Geometry
from OCC.Core.TopoDS import TopoDS_Shape

from pyoccad.transform import Move


class Scale:

    @staticmethod
    def from_factor(shape: Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape],
                    factor: float, inplace=True) -> Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape, None]:
        """Scale or create a scaled copy of a shape.

        Parameters
        ----------
        shape : Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape]
            The shape
        factor : float
            The scaling factor
        inplace: bool, optional
            Whether to apply the transformation inplace {Default=True}

        Returns
        -------
        scaled_shape : Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape, None]
            The resulting shape if inplace, else None
        """
        from pyoccad.create import CreateScaling

        return Move.using_transformation(shape, CreateScaling.from_factor(factor), inplace)
