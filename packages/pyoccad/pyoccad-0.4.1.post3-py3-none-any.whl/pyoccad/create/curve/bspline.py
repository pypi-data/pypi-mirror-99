from typing import Union, Sequence, Tuple

from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.Approx import Approx_Curve3d, Approx_CurvilinearParameter
from OCC.Core.Geom import Geom_BSplineCurve, Geom_Curve
from OCC.Core.Geom2d import Geom2d_Curve, Geom2d_BSplineCurve
from OCC.Core.Geom2dAPI import Geom2dAPI_PointsToBSpline, Geom2dAPI_Interpolate
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline, GeomAPI_Interpolate, geomapi
from OCC.Core.GeomAbs import GeomAbs_C0, GeomAbs_C1, GeomAbs_C2, GeomAbs_CN
from OCC.Core.Precision import precision
from OCC.Core.TColStd import TColStd_HArray1OfBoolean, TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt, TColgp_HArray1OfPnt2d
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire
from OCC.Core.gp import gp_Pln, gp_Pnt

from pyoccad.create import CreateVector, CreateCurve, CreateArray1, CreateHArray1
from pyoccad.typing import PointT, DirectionT

CONTINUITY_TYPES = {'c0': GeomAbs_C0,
                    'c1': GeomAbs_C1,
                    'c2': GeomAbs_C2}


class CreateBSpline:
    """Factory to create B-Spline curves.

    In the mathematical subfield of numerical analysis, a B-spline, or basis spline, is a spline function that has
    minimal support with respect to a given degree, smoothness, and domain partition.

    Any spline function of given degree can be expressed as a linear combination of B-splines of that degree.
    Cardinal B-splines have knots that are equidistant from each other.
    B-splines can be used for curve-fitting and numerical differentiation of experimental data.
    In computer-aided design and computer graphics, spline functions are constructed as linear combinations of B-splines
    with a set of control points.
    """

    @staticmethod
    def from_points(points: Sequence[PointT],
                    degrees: Tuple[int, int] = (3, 8),
                    tol: float = precision().Confusion(),
                    continuity: GeomAbs_CN = GeomAbs_C2) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Build a 2D/3D B-Spline curve passing through an array of points.

        Notes
        -----
        Approximates a BSpline CurveT passing through an array of points.

        The resulting BSpline will have the following properties:
            * its degree will be bounded by min and max degrees
            * its continuity will be at least <continuity>
            * the distance from the point <points> to the BSpline will be lower than tol.

        Parameters
        ----------
        points: Sequence[PointT]
            The control points
        degrees: Tuple[int, int], optional
            Minimal and maximal B-Spline degrees {default=(3, 8)}
        tol: float, optional
            Tolerance {Default=precision().Confusion()}
        continuity: GeomAbs_CN, optional
            Required continuity

        Returns
        -------
        bspline: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The resulting B-Spline

        """
        array = CreateArray1.of_points(points)
        min_degree, max_degree = degrees

        if isinstance(array, TColgp_Array1OfPnt2d):
            bspline = Geom2dAPI_PointsToBSpline(array, min_degree, max_degree, continuity, tol).Curve()
        else:
            bspline = GeomAPI_PointsToBSpline(array, min_degree, max_degree, continuity, tol).Curve()

        return bspline

    @staticmethod
    def from_points_with_params(points: Sequence[PointT], parameters: Sequence[float],
                                tol: float, degrees: Tuple[int, int] = (3, 8),
                                continuity: GeomAbs_CN = GeomAbs_C2) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Builds a 2D/3D B-Spline curve passing through an array of points associated with chosen parameters.

        Parameters
        ----------
        points: Sequence[PointT]
            The control points
        parameters: Sequence[float]
            The parameters
        tol: float
            Tolerance
        degrees: Tuple[int, int], optional
            Minimal and maximal B-Spline degrees {default=(3, 8)}
        continuity: GeomAbs_CN, optional
            Required continuity

        Returns
        -------
        bspline: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The B-Spline
        """
        array = CreateArray1.of_points(points)
        param = CreateArray1.of_floats(parameters)
        min_degree, max_degree = degrees

        if isinstance(array, TColgp_Array1OfPnt2d):
            bspline = Geom2dAPI_PointsToBSpline(array, param, min_degree, max_degree, continuity, tol).Curve()
        else:
            bspline = GeomAPI_PointsToBSpline(array, param, min_degree, max_degree, continuity, tol).Curve()

        return bspline

    @staticmethod
    def from_points_with_smoothing(points: Sequence[PointT],
                                   weights: Tuple[float, float, float],
                                   tol: float,
                                   max_degree: int = 8,
                                   continuity: GeomAbs_CN = GeomAbs_C2) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Approximate a 2D/3D BSpline CurveT passing through an array of PointT using variational smoothing algorithm

        Notes
        -----
        The algorithm attempts to minimize the additional criteria: W1*CurveLength + W2*Curvature + W3*Torsion.

        Parameters
        ----------
        points: Sequence[PointT, ...]
            The control points
        weights: Tuple[float, float, float]
            The weigths for smoothing algorithm: length, curvature and torsion
        tol: float
            Tolerance
        max_degree: int, optional
            Maximal B-Spline degree {default=8}
        continuity: GeomAbs_CN, optional
            Required continuity {default=GeomAbs_C2}

        Returns
        -------
        bspline: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The B-Spline

        """
        array = CreateArray1.of_points(points)
        w1, w2, w3 = weights
        if isinstance(array, TColgp_Array1OfPnt2d):
            bspline = Geom2dAPI_PointsToBSpline(array, w1, w2, w3, max_degree, continuity, tol).Curve()
        else:
            bspline = GeomAPI_PointsToBSpline(array, w1, w2, w3, max_degree, continuity, tol).Curve()

        return bspline

    @staticmethod
    def __init_points_interpolate(points: Sequence[PointT],
                                  tol: float, periodic: bool) -> Union[Geom2dAPI_Interpolate, GeomAPI_Interpolate]:
        """Create an interpolator of points.

        Parameters
        ----------
        points: Sequence[PointT]
            The points
        tol: float
            Algorithm tolerance
        periodic: bool
            Whether periodic or not

        Returns
        -------
        interpolator: Union[Geom2dAPI_Interpolate, GeomAPI_Interpolate]
            The resulting interpolator
        """
        harray = CreateHArray1.of_points(points)

        if isinstance(harray, TColgp_HArray1OfPnt2d):
            bspline = Geom2dAPI_Interpolate(harray, periodic, tol)
        else:
            bspline = GeomAPI_Interpolate(harray, periodic, tol)

        return bspline

    @staticmethod
    def __build_tangent_flag_harray(tangent_array: Sequence[DirectionT], tol: float) -> TColStd_HArray1OfBoolean:
        """Build a boolean array describing if the inputs vectors have norms (superior to tolerance) or not.

        Parameters
        ----------
        tangent_array: Sequence[DirectionT]
            The input array
        tol
            The threshold to declare a vector has norm or not

        Returns
        -------
        array: TColStd_HArray1OfBoolean
            The resulting boolean array
        """
        low = tangent_array.Lower()
        up = tangent_array.Upper()
        tangent_flag_harray = TColStd_HArray1OfBoolean(low, up)

        for i in range(low, up + 1):
            has_norm = tangent_array.Value(i).Magnitude() > tol
            tangent_flag_harray.Array1().SetValue(i, has_norm)

        return tangent_flag_harray

    @staticmethod
    def from_points_interpolate(points: Sequence[PointT],
                                tol: float, periodic: bool = False) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Builds a 2D/3D B-Spline curve passing through an array of points, using an interpolation algorithm
        which allows periodic curves.

        Parameters
        ----------
        points: Sequence[PointT]
            The control points
        tol: float
            Algorithm tolerance
        periodic: bool
            Whether the curve is periodic or not {default=False}

        Returns
        -------
        interpolation: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The resulting B-Spline
        """
        interpolation = CreateBSpline.__init_points_interpolate(points, tol, periodic)
        interpolation.Perform()
        return interpolation.Curve()

    @staticmethod
    def from_points_interpolate_with_bounds_control(points: Sequence[PointT],
                                                    tangents: Tuple[DirectionT, DirectionT],
                                                    tol: float,
                                                    directions_only: bool = True,
                                                    periodic=False) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Build a 2D/3D B-Spline curve passing through an array of points, using an interpolation algorithm
        which allows periodic curves and starting/ending tangent controls.

        Parameters
        ----------
        points: Sequence[gp_Pnt]
            The control points
        tangents: Tuple[DirectionT, DirectionT]
            Starting and ending tangents directions
        tol: float
            Tolerance
        directions_only: bool, optional
            Whether only the tangents directions are considered or not {default=True}
        periodic: bool, optional
            Whether the curve is periodic or not {default=False}

        Returns
        -------
        interpolation: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The resulting B-Spline
        """
        interpolation = CreateBSpline.__init_points_interpolate(points, tol, periodic)
        start_tangent, end_tangent = tangents
        t1 = CreateVector.from_point(start_tangent)
        t2 = CreateVector.from_point(end_tangent)
        interpolation.Load(t1, t2, directions_only)
        interpolation.Perform()

        return interpolation.Curve()

    @staticmethod
    def from_points_and_tangents_interpolate(points: Sequence[PointT],
                                             tangents: Sequence[DirectionT],
                                             tol: float,
                                             directions_only: bool = True,
                                             periodic=False) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Build a 2D/3D B-Spline curve passing through an array of points with given tangents, using an interpolation
        algorithm which allows periodic curves.

        Parameters
        ----------
        points: Sequence[PointT]
            The control points
        tangents: Sequence[DirectionT]
            Starting and ending tangents directions
        tol: float
            Tolerance
        directions_only: bool, optional
            Whether only the tangents directions are considered or not {default=True}
        periodic: bool, optional
            Whether the curve is periodic or not {default=False}

        Returns
        -------
        interpolation: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The resulting B-Spline
        """
        if len(points) != len(tangents):
            raise AttributeError('Points and tangents sequences should have the same lengths, '
                                 'got {} and {}'.format(len(points), len(tangents)))

        interpolation = CreateBSpline.__init_points_interpolate(points, tol, periodic)
        tangents_array = CreateArray1.of_vectors(tangents)
        tangents_flags = CreateBSpline.__build_tangent_flag_harray(tangents_array, tol)

        interpolation.Load(tangents_array, tangents_flags, directions_only)
        interpolation.Perform()

        return interpolation.Curve()

    @staticmethod
    def from_poles_and_degree(poles: Sequence[PointT],
                              degree: int,
                              periodic: bool = False) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Build a B-Spline curve 2D/3D  from poles and degree.

        Notes
        -----
        Multiplicities and knots are computed automatically following this method:
            * len(multiplicities) = degree + len(poles) + 1
            * each coefficient of multiplicities = 1
            * knots(i) = i / (len(knots) - 1.)

        Parameters
        ----------
        poles: Sequence[PointT]
            The control points
        degree: int
            The curve degree
        periodic: bool, optional
            Whether the curve is periodic or not {default=False}

        Returns
        -------
        bspline: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The resulting B-Spline
        """
        arr = CreateArray1.of_points(poles)
        if not periodic:
            m = degree + 1 + arr.Length()
        else:
            m = 1 + arr.Length()
        mult = TColStd_Array1OfInteger(1, m)
        knots = TColStd_Array1OfReal(1, m)
        for i in range(0, m):
            mult.SetValue(i + 1, 1)
            knots.SetValue(i + 1, i / (m - 1.))

        if isinstance(arr, TColgp_Array1OfPnt):
            bspline = Geom_BSplineCurve(arr, knots, mult, degree, periodic)
        else:
            bspline = Geom2d_BSplineCurve(arr, knots, mult, degree, periodic)

        return bspline

    @staticmethod
    def approximation(curve: Union[Geom_Curve, Geom2d_Curve, TopoDS_Edge, TopoDS_Wire, Adaptor3d_Curve],
                      tol: float,
                      order: str = "c2",
                      max_parameters: Tuple[int, int] = (10, 8),
                      curvilinear_abs=False) -> Union[Geom2d_BSplineCurve, Geom_BSplineCurve]:
        """Compute a B-Spline that approximates a given curve.

        Parameters
        ----------
        curve:  Union[Geom_Curve, Geom2d_Curve, TopoDS_Edge, TopoDS_Wire, Adaptor3d_Curve]
            The element to approximate
        tol: float
            Tolerance for computation
        order: str, optional
            Required continuity {default="c2"}
        max_parameters: Tuple[int, int], optional
            Maximum values for segments count and B-Spline degree {default=(10, 8)}
        curvilinear_abs: bool, optional
            Toggle option to build a curve parametrized by curvilinear abs {default=False}

        Returns
        -------
        bspline: Union[Geom2d_BSplineCurve, Geom_BSplineCurve]
            The resulting B-Spline
        """
        from pyoccad.measure import MeasurePoint

        curve_hadaptor = CreateCurve.as_adaptor_handler(curve)
        dim = MeasurePoint.dimension(curve_hadaptor.Value(curve_hadaptor.FirstParameter()))
        order_type = CONTINUITY_TYPES[order]
        max_segments, max_degree = max_parameters

        if dim == 2:
            plane = gp_Pln()
            crv3d = Geom_Curve.DownCast(geomapi.To3d(curve, plane))
            approx3d = CreateBSpline.approximation(crv3d, tol, order, max_parameters, curvilinear_abs)
            bspline = Geom2d_BSplineCurve.DownCast(geomapi.To2d(approx3d, plane))

        else:  # dim == 3
            if curvilinear_abs:
                bspline = Approx_CurvilinearParameter(curve_hadaptor, tol, order_type, max_segments, max_degree).Curve3d()
            else:
                bspline = Approx_Curve3d(curve_hadaptor, tol, order_type, max_segments, max_degree).Curve()

        return bspline
