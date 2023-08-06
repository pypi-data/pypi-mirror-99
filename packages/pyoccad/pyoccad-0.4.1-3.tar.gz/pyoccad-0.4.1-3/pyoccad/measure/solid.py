from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pnt


def volume(shape: TopoDS_Shape) -> float:
    """Compute the volume of a shape

    Parameters
    ----------
    shape: TopoDS_Shape
        The shape to measure

    Returns
    -------
    volume: float
        The shape volume
    """
    s_prop = GProp_GProps()
    brepgprop.VolumeProperties(shape, s_prop)
    return s_prop.Mass()


def center(shape: TopoDS_Shape) -> gp_Pnt:
    """Return the shape center of gravity.
    
    Parameters
    ----------
    shape: TopoDS_Shape
        The shape to measure
    
    Returns
    -------
    pc: gp_Pnt
        Center of mass
        
    """
    s_prop = GProp_GProps()
    brepgprop.SurfaceProperties(shape, s_prop)
    return s_prop.CentreOfMass()
