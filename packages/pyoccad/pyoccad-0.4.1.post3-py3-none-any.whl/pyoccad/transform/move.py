from typing import Union

from OCC.Core.Geom import Geom_Geometry
from OCC.Core.Geom2d import Geom2d_Geometry
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Trsf, gp_Trsf2d


class Move:
    """Factory to move shapes."""

    @staticmethod
    def using_transformation(shape: Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape],
                             transformation: Union[gp_Trsf, gp_Trsf2d, TopLoc_Location],
                             inplace=True) -> Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]:
        """Move or create a copy of a moved shape.

        Parameters
        ----------
        shape : Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape]
            The shape
        transformation : Union[gp_Trsf, gp_Trsf2d, TopLoc_Location]
            The transformation
        inplace : bool, optional
            Whether to make the transformation inplace {default=False}

        Returns
        -------
        geom : Union[Geom2d_Geometry, Geom_Geometry, TopoDS_Shape, None]
            Moved copy if the transformation is not inplace, or None
        """
        location = None
        if isinstance(transformation, gp_Trsf):
            location = TopLoc_Location(transformation)
        elif isinstance(transformation, TopLoc_Location):
            location = transformation
            transformation = location.Transformation()

        if isinstance(shape, Geom2d_Geometry):
            if isinstance(transformation, gp_Trsf):
                transformation = gp_Trsf2d(transformation)

        if not isinstance(transformation, (gp_Trsf, gp_Trsf2d)):
            raise TypeError('Transformation type not handled {}."'.format(type(transformation)))

        is_geom = (isinstance(shape, Geom_Geometry) and isinstance(transformation, gp_Trsf)) or \
                  (isinstance(shape, Geom2d_Geometry) and isinstance(transformation, gp_Trsf2d))
        is_topo = isinstance(shape, TopoDS_Shape) and isinstance(transformation, gp_Trsf) and location is not None

        if not (is_geom or is_topo):
            raise TypeError('Incompatible types between shape and transformation.')

        if inplace:
            if is_geom:
                shape.Transform(transformation)
            else:  # is_topo
                shape.Move(location)
        else:
            if is_geom:
                return shape.DownCast(shape.Transformed(transformation))
            # is_topo
            return shape.Moved(location)
