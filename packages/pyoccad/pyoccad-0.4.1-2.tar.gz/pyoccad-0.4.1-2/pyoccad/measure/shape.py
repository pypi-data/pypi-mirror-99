from collections.abc import Iterable as IterableT
from typing import Tuple, Union, Iterable

from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.Geom import Geom_Geometry
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pnt


def bounds(shape: Union[TopoDS_Shape, Iterable[TopoDS_Shape]]) -> Tuple[float]:
    """Compute the bounding coordinates of a shape.
    
    Parameters
    ----------
    shape: Union[TopoDS_Shape, Iterable[TopoDS_Shape]]
        The shapes to be analyzed

    Returns
    -------
    bounds: Tuple[float]
        The bounds of the shapes
    
    """
    from pyoccad.create import CreateTopology

    box = Bnd_Box()
    if isinstance(shape, IterableT):
        for s in shape:
            brepbndlib.Add(CreateTopology.as_shape(s), box)
    else:
        brepbndlib.Add(CreateTopology.as_shape(shape), box)
    return box.Get()


def distance(shape_1: Union[gp_Pnt, Geom_Curve, Geom_Surface, Adaptor3d_Curve, TopoDS_Shape],
             shape_2: Union[gp_Pnt, Geom_Curve, Geom_Surface, Adaptor3d_Curve, TopoDS_Shape]) -> float:
    """Compute the minimum distance between 2 shapes.
    
    Parameters
    ----------
    shape_1 : Union[gp_Pnt, Geom_Curve, Geom_Surface, Adaptor3d_Curve, TopoDS_Shape]
        First shape
    shape_2 : Union[gp_Pnt, Geom_Curve, Geom_Surface, Adaptor3d_Curve, TopoDS_Shape]
        Second shape
    
    Returns
    -------
    distance : float
        The minimum distance between the 2 shapes
    
    """
    from pyoccad.create import CreateTopology

    return BRepExtrema_DistShapeShape(CreateTopology.as_shape(shape_1), CreateTopology.as_shape(shape_2)).Value()


def encompassing_sphere_diameter(sh_list: Iterable[Union[TopoDS_Shape, Geom_Geometry]]) -> float:
    """Find the diameter of a sphere encompassing the shape(s).
    
    Parameters
    ----------
    sh_list : Union[TopoDS_Shape, Geom_Geometry, Iterable[TopoDS_Shape, Geom_Geometry]]
        The entities to encompass
    
    Returns
    -------
    diameter : float
        The diameter of the encompassing sphere
    """
    xmin, ymin, zmin, xmax, ymax, zmax = bounds(sh_list)
    return max([xmax - xmin, ymax - ymin, zmax - zmin])
