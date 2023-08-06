from OCC.Core.Adaptor3d import Adaptor3d_Surface, Adaptor3d_HSurface
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.Geom import Geom_Surface
from OCC.Core.GeomAdaptor import GeomAdaptor_Surface
from OCC.Core.TopoDS import TopoDS_Face

from pyoccad.typing import Surface3D


class CreateSurface:
    """Factory to create surfaces."""

    @staticmethod
    def as_adaptor(surface: Surface3D) -> Adaptor3d_Surface:
        """Create a surface adaptor.

        Parameters
        ----------
        surface: Union[Geom_Surface, TopoDS_Face]
            The surface

        Returns
        -------
        adaptor: Adaptor3d_Surface
            The resulting adaptor
        """
        if isinstance(surface, Geom_Surface):
            return GeomAdaptor_Surface(surface)
        if isinstance(surface, TopoDS_Face):
            return BRepAdaptor_Surface(surface)
        if isinstance(surface, Adaptor3d_Surface):
            return surface
        if isinstance(surface, Adaptor3d_HSurface):
            return surface.Surface()

        raise TypeError('Unsupported type "{}".'.format(type(surface)))
