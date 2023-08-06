from typing import Union

from OCC.Core.Geom import Geom_Geometry
from OCC.Core.Geom2d import Geom2d_Geometry
from OCC.Core.TopoDS import TopoDS_Shape

from pyoccad.transform import Move
from pyoccad.typing import VectorT


class Translate:

    @staticmethod
    def from_vector(shape: Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape],
                    vector: VectorT, inplace=True) -> Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape, None]:
        """Translate or create a translated copy of a shape.

        Parameters
        ----------
        shape : Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape]
            The shape
        vector : VectorT
            The translation vector
        inplace: bool, optional
            Whether to apply the transformation inplace {Default=True}

        Returns
        -------
        translated_shape : Union[Geom_Geometry, Geom2d_Geometry, TopoDS_Shape, None]
            The resulting shape if inplace, else None
        """
        from pyoccad.create import CreateTranslation

        return Move.using_transformation(shape, CreateTranslation.from_vector(vector), inplace)
