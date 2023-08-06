from typing import Union, Sequence, Tuple

import numpy as np
from OCC.Core.GC import GC_MakeCircle
from OCC.Core.GCE2d import GCE2d_MakeCircle
from OCC.Core.GccEnt import GccEnt_unqualified
from OCC.Core.Geom import Geom_Circle
from OCC.Core.Geom2d import Geom2d_TrimmedCurve, Geom2d_CartesianPoint, Geom2d_Point, Geom2d_Circle, Geom2d_Curve
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.Core.Geom2dGcc import Geom2dGcc_Circ2d2TanOn, Geom2dGcc_QualifiedCurve, Geom2dGcc_Circ2d3Tan, \
    Geom2dGcc_Circ2dTanCen, Geom2dGcc_Circ2d2TanRad
from OCC.Core.GeomAPI import geomapi
from OCC.Core.gp import gp_Ax2, gp_Pnt2d, gp_Pln, gp_Circ, gp_Circ2d, gp_Ax3

from pyoccad.create import CreateDirection, CreatePoint, CreateCurve, CreateLine
from pyoccad.typing import PointT, DirectionT


class CreateCircle:
    """Factory for circle creation."""

    @staticmethod
    def from_3_points(points: Tuple[PointT, PointT, PointT]) -> Geom_Circle:
        """Create a circle passing by 3 points.

        Parameters
        ----------
        points: Sequence[PointT, PointT, PointT]
            The sequence of 3 points required to create the circle

        Returns
        -------
        circle: Geom_Circle
            The resulting circle
        """
        if len(points) != 3:
            raise AttributeError('3 points should be provided, got {}.'.format(len(points)))

        points_adaptor = [CreatePoint.as_point(point_) for point_ in points]
        return GC_MakeCircle(*points_adaptor).Value()

    @staticmethod
    def from_radius_and_center(radius: float,
                               center: PointT = (0, 0, 0),
                               normal: DirectionT = (0, 0, 1)) -> Union[Geom2d_Circle, Geom_Circle]:
        """Create a circle with a radius r around a point center, in a plane defined by a normal vector.

        Parameters
        ----------
        radius: float
            The circle radius
        center: PointT, optional
            The center of the circle {default=(0., 0., 0.)}
        normal: DirectionT, optional
            The normal vector {default=(0., 0., 1.)}

        Returns
        -------
        circle: Union[Geom2d_Circle, Geom_Circle]
            The resulting circle
        """
        from pyoccad.measure import MeasurePoint

        dim = MeasurePoint.dimension(center)
        if dim == 2:
            circle = GCE2d_MakeCircle(CreatePoint.as_point(center), radius).Value()
        else:
            circle = GC_MakeCircle(CreatePoint.as_point(center), CreateDirection.as_direction(normal), radius).Value()
        return circle

    @staticmethod
    def from_radius_and_axis(radius: float, axis: gp_Ax2) -> Geom_Circle:
        """Create a circle rotating around an axis with a given radius.

        Parameters
        ----------
        radius: float
            The circle radius
        axis: gp_Ax2
            AxisT used to define the circle centre and direction

        Returns
        -------
        circle: Geom_Circle
            The resulting circle
        """
        return GC_MakeCircle(axis, radius).Value()

    @staticmethod
    def __get_gcc_circle_solutions(gcc: Geom2dGcc_Circ2d2TanOn) -> Sequence[Geom2d_Circle]:
        """Get the solutions from an OpenCascade container.

        Parameters
        ----------
        gcc: Geom2dGcc_Circ2d2TanOn
            The OpenCascade container of solutions

        Returns
        -------
        solutions: Sequence[Geom2d_Circle]
            A Python sequence of solutions
        """
        length = gcc.NbSolutions()

        if length == 0:
            raise AttributeError('No solution found.')

        if not gcc.IsDone():
            raise AttributeError('{} solutions founds with errors.'.format(length))

        solutions = [GCE2d_MakeCircle(gcc.ThisSolution(i)).Value() for i in range(1, length + 1)]
        return solutions

    @staticmethod
    def __bi_tangent_solutions_with_position(curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                             curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                             parameter1: float, tol: float,
                                             parameter2: float = None) -> Sequence[Geom2d_Circle]:
        """Find a list of possible bi-tangent circles on 2 curves.

        Parameters
        ----------
        curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            First curve
        curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            Second curve
        parameter1: float
            Position on first curve
        tol: float
            Tolerance on solutions
        parameter2: float, optional
            Guessed position on second curve {default=None}

        Returns
        -------
        solutions:  Sequence[Geom2d_Circle]
            The solutions found
        """
        from pyoccad.measure import MeasureExtrema

        line_ = CreateLine.normal_to_curve(curve1, parameter1)
        u1 = parameter1

        try:
            line_max_parameter, u2, pt1, pt2 = MeasureExtrema.between_2_curves(line_, curve2, True, tol)
            trimmed_line = Geom2d_TrimmedCurve(line_, 0, line_max_parameter)
        except ArithmeticError:
            u2 = parameter1
            line_max_parameter = 0
            trimmed_line = Geom2d_TrimmedCurve(line_, -1e30, 1e30)

        if parameter2 is not None:
            u2 = parameter2

        trimmed_line_adaptor = Geom2dAdaptor_Curve(trimmed_line)

        # TODO trys to extend crv2
        # crv2_3d = geomapi.To3d(crv2_2d ,gp_Pln() )
        # geomlib.ExtendCurveToPoint()

        curve1_qualified = Geom2dGcc_QualifiedCurve(CreateCurve.as_adaptor(curve1), GccEnt_unqualified)
        curve2_qualified = Geom2dGcc_QualifiedCurve(CreateCurve.as_adaptor(curve2), GccEnt_unqualified)

        gcc = Geom2dGcc_Circ2d2TanOn(curve1_qualified, curve2_qualified, trimmed_line_adaptor,
                                     tol, parameter1, u2, abs(line_max_parameter / 2.))
        return CreateCircle.__get_gcc_circle_solutions(gcc)

    @staticmethod
    def __get_extrema(solutions: Sequence[Geom2d_Circle], use_smallest: bool) -> Geom2d_Circle:
        """Get the extrema solution from a sequence of solutions.

        Parameters
        ----------
        solutions: Sequence[Geom2d_Circle]
            All the possible solutions
        use_smallest: bool
            Whether to use the smallest or the largest solution

        Returns
        -------
        extrema: Geom2d_Circle
            The extrema solution
        """

        if len(solutions) == 0:
            raise ArithmeticError('No solution found')

        radii = [solution.Radius() for solution in solutions]
        if use_smallest:
            position = np.argmin(radii)
        else:
            position = np.argmax(radii)

        return solutions[int(position)]

    @staticmethod
    def bi_tangent_with_position(curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                 curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                 parameter1: float, tol: float,
                                 parameter2: float = None, use_smallest: bool = True) -> Geom2d_Circle:
        """Build a 2D circle tangent to 2 curves for a given position on the first curve.

        Parameters
        ----------
        curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            First curve
        curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            Second curve
        parameter1: float
            Position on first curve
        tol: float
            Tolerance on solution
        parameter2: float, optional
            Guessed position on second curve {default=None}
        use_smallest: bool, optional
            In case of multiple solutions, whether to use the smallest or biggest (False) {default=True}

        Returns
        -------
        solution: Geom2d_Circle
            The solution found
        """

        solutions = CreateCircle.__bi_tangent_solutions_with_position(curve1, curve2, parameter1, tol, parameter2)
        return CreateCircle.__get_extrema(solutions, use_smallest)

    @staticmethod
    def __bi_tangent_solutions_with_radius(curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                           curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                           radius: float, tol: float) -> Sequence[Geom2d_Circle]:
        """Find a list of possible bi-tangent circles on 2 curves with a given radius.

         Parameters
         ----------
         curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
             First curve
         curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
             Second curve
         radius: float
             Radius of the circle
         tol: float
             Tolerance on solutions

         Returns
         -------
         solutions:  Sequence[Geom2d_Circle]
             The solutions found
         """

        if isinstance(curve1, Geom2dAdaptor_Curve):
            curve1_adaptor = curve1
        else:
            curve1_adaptor = Geom2dAdaptor_Curve(curve1)

        if isinstance(curve2, Geom2dAdaptor_Curve):
            curve2_adaptor = curve2
        else:
            curve2_adaptor = Geom2dAdaptor_Curve(curve2)

        curve1_qualified = Geom2dGcc_QualifiedCurve(curve1_adaptor, GccEnt_unqualified)
        curve2_qualified = Geom2dGcc_QualifiedCurve(curve2_adaptor, GccEnt_unqualified)
        gcc = Geom2dGcc_Circ2d2TanRad(curve1_qualified, curve2_qualified, radius, tol)
        return CreateCircle.__get_gcc_circle_solutions(gcc)

    @staticmethod
    def bi_tangent_with_radius(curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                               curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                               radius: float, tol: float, use_smallest: bool = True) -> Geom2d_Circle:
        """Builds a 2d circle tangent to 2 curves with given radius

        Parameters
        ----------
         curve1: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
             First curve
         curve2: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
             Second curve
         radius: float
             Radius of the circle
         tol: float
             Tolerance on solutions
        use_smallest: bool, optional
            In case of multiple solutions, whether to use the smallest or biggest (False) {default=True}

        Returns
        -------
        solution: Geom2d_Circle
            The solution found
        """
        solutions = CreateCircle.__bi_tangent_solutions_with_radius(curve1, curve2, radius, tol)
        return CreateCircle.__get_extrema(solutions, use_smallest)

    @staticmethod
    def __tri_tangent_solutions(curves: Tuple[Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                              Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                              Union[Geom2d_Curve, Geom2dAdaptor_Curve]],
                                tol: float,
                                guess_parameters: Tuple[float, float, float] = (0., 0., 0.)) -> Sequence[Geom2d_Circle]:
        """Find tri-tangent solutions to 3 curves.

        Parameters
        ----------
        curves: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            The 3 curves
        tol: float
            Tolerance on solutions
        guess_parameters: Tuple[float, float, float], optional
            Guess positions on the curves {default=(0., 0., 0.)}

        Returns
        -------
        solutions:  Sequence[Geom2d_Circle]
            The solutions found
        """
        curve1, curve2, curve3 = curves
        curve1_qualifier = Geom2dGcc_QualifiedCurve(Geom2dAdaptor_Curve(curve1), GccEnt_unqualified)
        curve2_qualifier = Geom2dGcc_QualifiedCurve(Geom2dAdaptor_Curve(curve2), GccEnt_unqualified)
        curve3_qualifier = Geom2dGcc_QualifiedCurve(Geom2dAdaptor_Curve(curve3), GccEnt_unqualified)
        u1, u2, u3 = guess_parameters

        gcc = Geom2dGcc_Circ2d3Tan(curve1_qualifier, curve2_qualifier, curve3_qualifier, tol,
                                   u1, u2, u3)
        return CreateCircle.__get_gcc_circle_solutions(gcc)

    @staticmethod
    def tri_tangent(curves: Tuple[Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                  Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                  Union[Geom2d_Curve, Geom2dAdaptor_Curve]],
                    tol,
                    guess_parameters: Tuple[float, float, float] = (0., 0., 0.),
                    use_smallest=True) -> Geom2d_Circle:
        """Build a 2D circle tangent to 3 curves.

        Parameters
        ----------
        curves: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            The 3 curves
        tol: float
            Tolerance on solutions
        guess_parameters: Tuple[float, float, float], optional
            Guess positions on the curves {default=(0., 0., 0.)}
        use_smallest: bool, optional
            In case of multiple solutions, whether to use the smallest or biggest (False) {default=True}

        Returns
        -------
        solution: Geom2d_Circle
            The solution found
        """
        solutions = CreateCircle.__tri_tangent_solutions(curves, tol, guess_parameters)
        return CreateCircle.__get_extrema(solutions, use_smallest)

    @staticmethod
    def __tangent_and_center_solutions(curve: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                                       center: PointT, tol: float) -> Sequence[Geom2d_Circle]:
        """

        Parameters
        ----------
        curve: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            The curve to tangent
        center: PointT
            The center of the circle
        tol: float
            Tolerance on solutions

        Returns
        -------
        solutions:  Sequence[Geom2d_Circle]
            The solutions found
        """
        curve_adaptor = Geom2dAdaptor_Curve(curve)
        curve_qualified = Geom2dGcc_QualifiedCurve(curve_adaptor, GccEnt_unqualified)

        if isinstance(center, Geom2d_Point):
            gcc = Geom2dGcc_Circ2dTanCen(curve_qualified, center, tol)
        elif isinstance(center, gp_Pnt2d):
            gcc = Geom2dGcc_Circ2dTanCen(curve_qualified, Geom2d_CartesianPoint(center), tol)
        else:
            gcc = Geom2dGcc_Circ2dTanCen(curve_qualified, Geom2d_CartesianPoint(CreatePoint.as_point(center)), tol)

        return CreateCircle.__get_gcc_circle_solutions(gcc)

    @staticmethod
    def tangent_and_center(curve: Union[Geom2d_Curve, Geom2dAdaptor_Curve],
                           center: PointT, tol: float, use_smallest: bool = True) -> Geom2d_Circle:
        """Builds a 2d circle tangent to a curve with specified center

        Parameters
        ----------
        curve: Union[Geom2d_Curve, Geom2dAdaptor_Curve]
            The curve to tangent
        center: PointT
            The center of the circle
        tol: float
            Tolerance on solutions
        use_smallest: bool, optional
            In case of multiple solutions, whether to use the smallest or biggest (False) {default=True}

        Returns
        -------
        solution: Geom2d_Circle
            The solution found
        """
        solutions = CreateCircle.__tangent_and_center_solutions(curve, center, tol)
        return CreateCircle.__get_extrema(solutions, use_smallest)

    @staticmethod
    def from_3d(circle: Union[gp_Circ, Geom_Circle]) -> Union[gp_Circ2d, Geom2d_Circle]:
        """Create a 2D circle from a 3D one.

        Parameters
        ----------
        circle: Union[gp_Circ, Geom_Circle]
            The 3D circle to be transformed

        Returns
        -------
        circle_2d: Union[gp_Circ2d, Geom2d_Circle]
            The resulting 2D circle
        """
        if isinstance(circle, Geom_Circle):
            pln = gp_Pln(gp_Ax3(circle.Circ().Position()))
            return Geom2d_Circle.DownCast(geomapi.To2d(circle, pln))
        if isinstance(circle, gp_Circ):
            return CreateCircle.from_3d(Geom_Circle(circle)).Circ2d()

        raise TypeError('Type "{}" not handled.'.format(type(circle)))

    @staticmethod
    def from_2d(circle: Union[gp_Circ2d, Geom2d_Circle], pln: gp_Pln = gp_Pln()) -> Union[gp_Circ, Geom_Circle]:
        """Create a 3D circle from a 2D one.

        Parameters
        ----------
        circle: Union[gp_Circ2d, Geom2d_Circle]
            The 2D circle to be transformed
        pln: gp_Pln, optional
            The plane where the 2D circle lies

        Returns
        -------
        circle_3d: Union[gp_Circ, Geom_Circle]
            The resulting 3D circle
        """
        if isinstance(circle, Geom2d_Circle):
            return Geom_Circle.DownCast(geomapi.To3d(circle, pln))
        if isinstance(circle, gp_Circ2d):
            return Geom_Circle.DownCast(CreateCircle.from_2d(Geom2d_Circle(circle), pln)).Circ()

        raise TypeError('Type "{}" not handled.'.format(type(circle)))