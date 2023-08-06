from typing import Union, Tuple, List

import numpy as np
from OCC.Core.Adaptor2d import Adaptor2d_Curve2d, Adaptor2d_HCurve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_HCurve, Adaptor3d_Surface, Adaptor3d_HSurface
from OCC.Core.BRepAdaptor import BRepAdaptor_HCurve, BRepAdaptor_HCompCurve, BRepAdaptor_Curve, BRepAdaptor_CompCurve
from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Face
from OCC.Core.gp import gp_Pnt2d, gp_Pnt, gp_Dir, gp_Dir2d, gp_Ax1, gp_Ax2d, gp_Ax2, gp_Ax3, gp_Ax22d, \
    gp_XY, gp_XYZ, gp_Vec, gp_Vec2d

Point2T = Union[gp_XY, gp_Pnt2d, gp_Vec2d, Tuple[float, float], List[float], np.ndarray]
"""All the possible 2D point types"""
Point3T = Union[gp_XYZ, gp_Pnt, gp_Vec, Tuple[float, float, float], List[float], np.ndarray]
"""All the possible 3D point types"""
PointT = Union[Point2T, Point3T]
"""All the possible point types"""

Direction2T = Union[gp_Dir2d, Point2T]
"""All the possible 2D direction types"""
Direction3T = Union[gp_Dir, Point3T]
"""All the possible 3D direction types"""
DirectionT = Union[Direction2T, Direction3T]
"""All the possible direction types"""

Vector2T = Union[gp_Vec2d, Tuple[Point2T, Point2T], Direction2T, Tuple[Direction2T, float]]
"""All the possible 2D vector types"""
Vector3T = Union[gp_Vec, Tuple[Point3T, Point3T], Direction3T, Tuple[Direction3T, float]]
"""All the possible 3D vector types"""
VectorT = Union[Vector2T, Vector3T]
"""All the possible vector types"""
OccVector = Union[gp_Vec2d, gp_Vec]
"""All the possible OpenCascade vector types"""

Axis2T = Union[gp_Ax2d, Tuple[Point2T, Direction2T]]
Axis3T = Union[gp_Ax1, Tuple[Point3T, Direction3T]]
AxisT = Union[Axis2T, Axis3T]
"""All the possible axis types"""

CoordSystem2T = Union[gp_Ax22d, Tuple[Point2T, Direction2T, Direction2T]]
CoordSystem3T = Union[gp_Ax2, gp_Ax3, Tuple[Point3T, Direction3T, Direction3T]]
CoordSystemT = Union[CoordSystem2T, CoordSystem3T]
"""All the possible coordinate system types"""

CurveAdaptor2T = Adaptor2d_Curve2d
CurveAdaptor3T = Union[Adaptor3d_Curve, BRepAdaptor_Curve, BRepAdaptor_CompCurve]
CurveAdaptorT = Union[CurveAdaptor2T, CurveAdaptor3T]
"""All the possible curve adaptor types"""
CurveAdaptorHandler2T = Adaptor2d_HCurve2d
CurveAdaptorHandler3T = Union[Adaptor3d_HCurve, BRepAdaptor_HCurve, BRepAdaptor_HCompCurve]
CurveAdaptorHandlerT = Union[CurveAdaptorHandler2T, CurveAdaptorHandler3T]
"""All the possible curve adaptor handler types"""
OccCurve2T = Geom2d_Curve
OccCurve3T = Union[Geom_Curve, TopoDS_Edge, TopoDS_Wire]
OccCurveT = Union[OccCurve2T, OccCurve3T]
"""All the possible OpenCascade curve types"""
Curve2T = Union[OccCurve2T, CurveAdaptor2T, CurveAdaptorHandler2T]
Curve3T = Union[OccCurve3T, CurveAdaptor3T, CurveAdaptorHandler3T]
CurveT = Union[Curve2T, Curve3T]
"""All the possible curve types"""

Surface3D = Union[Geom_Surface, TopoDS_Face, Adaptor3d_Surface, Adaptor3d_HSurface]
