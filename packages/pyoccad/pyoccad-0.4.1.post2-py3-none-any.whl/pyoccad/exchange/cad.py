"""Interface module to export the geometric entities to external formats.

"""

import os
from typing import Union, Iterable

from OCC.Core.Geom import Geom_Geometry
from OCC.Core.IGESControl import IGESControl_Controller, IGESControl_Writer
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.TopoDS import TopoDS_Shape


def to_iges(shapes: Iterable[Union[Geom_Geometry, TopoDS_Shape]], file_name: str,
            scale_factor: float = 1000.) -> bool:
    """Export shapes to iges file

    Parameters
    ----------
    shapes : Iterable[Union[Geom_Geometry, TopoDS_Shape]]
        The shapes to export
    file_name : str
        File name, the extension is automatically set to .igs
    scale_factor : float, optional
        Scale factor, iges files are in millimeters (default: {1000})

    Returns
    -------
    success : bool
        True if written with success
    """
    from pyoccad.transform import Scale

    IGESControl_Controller().Init()
    writer = IGESControl_Writer('MM', 0)

    for shape in shapes:
        if isinstance(shape, Geom_Geometry):
            writer.AddGeom(Scale.from_factor(shape, scale_factor, False))
        elif isinstance(shape, TopoDS_Shape):
            writer.AddShape(Scale.from_factor(shape, scale_factor, False))
        else:
            raise TypeError('Unsupported type "{}"'.format(type(shape)))

    writer.ComputeModel()

    pre, ext = os.path.splitext(file_name)
    if ext is not ".igs":
        file_name = pre + ".igs"
    return writer.Write(file_name)


# TODO: add mode enum visible/wrapped from occt
def to_step(shapes: Iterable[TopoDS_Shape], file_name: str, mode = STEPControl_AsIs,
            scale_factor: float = 1000.):
    """Export shapes to step file

    Parameters
    ----------
    shapes : Iterable[TopoDS_Shape]
        The shapes to save
    file_name : str
        File name, the extension is automatically set to .step
    mode :
    scale_factor : float, optional
        Scale factor, step files are in millimeters (default: {1000})

    Returns
    -------
    flag : bool
        True if written with success
        
    """
    from pyoccad.transform import Scale

    writer = STEPControl_Writer()
    for shape in shapes:
        if isinstance(shape, TopoDS_Shape):
            writer.Transfer(Scale.from_factor(shape, scale_factor, False), mode)
        else:
            raise TypeError('Unsupported type "{}"'.format(type(shape)))

    pre, ext = os.path.splitext(file_name)
    if ext is not ".stp":
        file_name = pre + ".stp"
    return writer.Write(file_name)
