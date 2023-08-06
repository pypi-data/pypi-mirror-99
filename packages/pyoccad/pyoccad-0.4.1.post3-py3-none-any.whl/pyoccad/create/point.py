from typing import Union, List, Tuple, Sequence

import numpy as np
from OCC.Core.Adaptor2d import Adaptor2d_Curve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Plane, Geom_Curve
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Vertex
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_XY, gp_XYZ, gp_Vec, gp_Pln, gp_Vec2d

from pyoccad.typing import PointT, CoordSystemT


class CreatePoint:
    """Factory to create points."""

    @staticmethod
    def as_point(point: PointT) -> Union[gp_Pnt, gp_Pnt2d]:
        """Create a 2D/3D point.

        Parameters
        ----------
        point: pyoccad.types.PointT
            The coordinates

        Returns
        -------
        point: Union[gp_Pnt, gp_Pnt2d]
            The resulting point
        """
        if isinstance(point, (gp_Pnt, gp_Pnt2d)):
            return point

        if isinstance(point, (gp_Vec, gp_XYZ)):
            return gp_Pnt(*point.Coord())

        if isinstance(point, (gp_Vec2d, gp_XY)):
            return gp_Pnt2d(*point.Coord())

        if isinstance(point, np.ndarray):
            dimension = point.size
            if not (2 <= dimension <= 3 and point.ndim == 1):
                raise TypeError('PointT should have dimension 2 or 3, got {}.'.format(dimension))
            point = point.tolist()

        if isinstance(point, (tuple, list)):
            dimension = len(point)
            types = [type(element) for element in point]
            unique_types = set(types)

            if unique_types.issubset({float, int, np.float_, np.int_}):
                if dimension == 3:
                    return gp_Pnt(*point)
                if dimension == 2:
                    return gp_Pnt2d(*point)
                raise TypeError('Exactly 2 or 3 coordinates expected to define a point, '
                                'got {}.'.format(dimension))

            raise TypeError('PointT coordinates have unsupported type(s): should be int or float, '
                            'got {}.'.format(unique_types))

        raise TypeError('PointT type not handled.')

    @staticmethod
    def as_list(point: PointT) -> List[float]:
        """Convert a point into a Python list.

        Parameters
        ----------
        point: PointT
            The point

        Returns
        -------
        list: List[float]
            A Python list of coordinates
        """
        return [*CreatePoint.as_point(point).Coord()]

    @staticmethod
    def as_tuple(point: PointT) -> Union[Tuple[float, float], Tuple[float, float, float]]:
        """Convert a point into a Python tuple.

        Parameters
        ----------
        point: PointT
            The point

        Returns
        -------
        tuple: Union[Tuple[float, float], Tuple[float, float, float]]
            A Python tuple of coordinates
        """
        return CreatePoint.as_point(point).Coord()

    @staticmethod
    def as_ndarray(point: PointT) -> np.ndarray:
        """Convert a point into a Numpy ndarray.

        Parameters
        ----------
        point: PointT
            The point

        Returns
        -------
        ndarray: np.ndarray
            A point formatted with Numpy ndarray of coordinates
        """
        return np.array(CreatePoint.as_point(point).Coord())

    @staticmethod
    def from_vertex(vertex: TopoDS_Vertex) -> gp_Pnt:
        if isinstance(vertex, TopoDS_Vertex):
            return BRep_Tool.Pnt(vertex)

        raise TypeError('Type of vertex should be "TopoDS_Vertex", got {}.'.format(type(vertex)))

    @staticmethod
    def from_cylindrical(point: PointT, referential: CoordSystemT) -> Union[gp_Pnt, gp_Pnt2d]:
        """Create a 3D point from a cylindrical description and a referential.

        Parameters
        ----------
        point: PointT
            The cylindrical description of the point
        referential: Referential_3d
            The referential for the conversion

        Returns
        -------
        cartesian_point: Union[gp_Pnt, gp_Pnt2d]
            The resulting point
        """
        from pyoccad.measure.coord_system import MeasureCoordSystem

        point = CreatePoint.as_point(point)
        if isinstance(point, gp_Pnt):
            dimension = 3
        else:
            dimension = 2

        referential_dimension = MeasureCoordSystem.dimension(referential)

        if referential_dimension != dimension:
            raise AttributeError('PointT and referential dimensions should match, '
                                 'got {} and {}.'.format(dimension, referential_dimension))

        if dimension == 3:
            cartesian_point = referential.Location()
            cartesian_point.Translate(gp_Vec(referential.XDirection()) * point.X())
            cartesian_point.Translate(gp_Vec(referential.Direction()) * point.Z())
            cartesian_point.Rotate(referential.Axis(), point.Y())
        else:
            cartesian_point = referential.Location()
            cartesian_point.Translate(gp_Vec2d(referential.XDirection()) * point.X())
            cartesian_point.Rotate(referential.Location(), point.Y())
        return cartesian_point

    @staticmethod
    def from_curve(curve: Union[Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve],
                   parameter: float) -> Union[gp_Pnt, gp_Pnt2d]:
        """Provide the point located on a curve a at given parameter.

        Parameters
        ----------
        curve: Union[Adaptor3d_Curve, Geom_Curve, Adaptor2d_Curve2d, Geom2d_Curve]
            The curve
        parameter: float
            The position on the curve

        Returns
        -------
        point: Union[gp_Pnt, gp_Pnt2d]
            The resulting point
        """
        return curve.Value(parameter)

    @staticmethod
    def from_curve_relative_pos(curve: Union[Geom_Curve, TopoDS_Edge, TopoDS_Wire, Adaptor3d_Curve],
                                position: float) -> gp_Pnt:
        """Get a point at a curve curvilinear position.

        Parameters
        ----------
        curve: Union[Geom_Curve, TopoDS_Edge, TopoDS_Wire, Adaptor3d_Curve]
            The curve
        position: float
            The curvilinear position on the curve

        Returns
        -------
        point: gp_Pnt
            The resulting point
        """
        from pyoccad.measure import MeasureCurve

        u = MeasureCurve.position_from_relative_curvilinear_abs(curve, position)
        return CreatePoint.from_curve(curve, u)

    @staticmethod
    def projected_on_plane(point: gp_Pnt, plane: gp_Pln) -> gp_Pnt:
        """Build a projection of point on plane.

        Parameters
        ----------
        point: gp_Pnt
            The point to project
        plane: gp_Pln
            The projection plane

        Returns
        -------
        projected_point: gp_Pnt
            The projected point
        """
        g_pln = Geom_Plane(plane)
        return GeomAPI_ProjectPointOnSurf(point, g_pln).NearestPoint()

    @staticmethod
    def centroid(points: Sequence[PointT]) -> Union[gp_Pnt2d, gp_Pnt]:
        """Compute the centroid of points.

        Parameters
        ----------
        points: Sequence[PointT]
            The input points

        Returns
        -------
        pnt: Union[gp_Pnt2d, gp_Pnt]
            The centroid point
        """
        points_count = len(points)
        weighting = np.ones(points_count) / points_count
        return CreatePoint.barycenter(list(points), weighting)

    @staticmethod
    def barycenter(points: Sequence[PointT], weighting: Sequence[float]) -> Union[gp_Pnt, gp_Pnt2d]:
        """Computes the point between two points, weighted by a factor k1.

        Notes
        -----
        Pnt = k1 * p1 + (1 - k1) * p2

        Parameters
        ----------
        points: Sequence[PointT]
            The first point
        weighting: Sequence[float]
            The weighting factors

        Returns
        -------
        point: Union[gp_Pnt, gp_Pnt2d]
            The barycenter
        """
        weighting = np.array(weighting) / np.sum(weighting)
        barycenter = np.dot(weighting, np.array([CreatePoint.as_point(p).Coord() for p in points]))
        return CreatePoint.as_point(barycenter)

    @staticmethod
    def as_point_in_referential(point: PointT, referential: CoordSystemT) -> Union[gp_Pnt, gp_Pnt2d]:
        """Create a 2D/3D point in a specific referential.

        Parameters
        ----------
        point: PointT
            The point coordinates
        referential: CoordSystemT
            The referential

        Returns
        -------
        point: Union[gp_Pnt, gp_Pnt2d]
            The computed point
        """
        from pyoccad.measure.coord_system import MeasureCoordSystem

        point_ = CreatePoint.as_point(point)
        if isinstance(point_, gp_Pnt):
            dimension = 3
        else:
            dimension = 2
        referential_dimension = MeasureCoordSystem.dimension(referential)

        if referential_dimension != dimension:
            raise AttributeError('PointT and referential dimensions should match, '
                                 'got {} and {}.'.format(dimension, referential_dimension))

        if dimension == 3:
            new_point = referential.Location().XYZ() + \
                        referential.XDirection().XYZ() * point_.X() + \
                        referential.YDirection().XYZ() * point_.Y() + \
                        referential.Direction().XYZ() * point_.Z()

            new_point = CreatePoint.as_point(new_point)
        else:
            new_point = referential.Location().XY() + \
                        referential.XDirection().XY() * point_.X() + \
                        referential.YDirection().XY() * point_.Y()

            new_point = CreatePoint.as_point(new_point)

        return new_point
