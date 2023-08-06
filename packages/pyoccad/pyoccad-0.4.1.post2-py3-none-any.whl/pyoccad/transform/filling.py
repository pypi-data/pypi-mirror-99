from typing import List, Tuple

from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.Geom import Geom_BSplineSurface
# from OCC.Core.GeomFill import GeomFill_NSections
from OCC.Core.TopoDS import TopoDS_Shape


class Filling:

    @staticmethod
    def from_curves(curves: List) -> Geom_BSplineSurface:
        # TODO: not working, TColGeom_SequenceOfCurve not correcly wrapped
        """Fill the curves with a surface.

        Parameters
        ----------
        curves: list
            The list of curves to fill

        Returns
        -------
        surface: Geom_BSplineSurface
            The resulting surface
        """
        from pyoccad.create import CreateSequence

        nc = CreateSequence.of_curves(curves)
        geom_fill = GeomFill_NSections(nc)
        return geom_fill.BSplineSurface()

    @staticmethod
    def from_profiles(profile_lst: List, tol: float = 1e-6, build_solid: bool = False, use_smoothing: bool = False,
                      w: Tuple = (1., 1., 1.), max_deg: int = 8) -> TopoDS_Shape:
        """Create a loft.

        Notes
        -----
        A loft is a shell or a solid passing through a set of profiles in a given sequence.
        Profiles have to be converted to wires

        Parameters
        ----------
        profile_lst: {container of linear elements}
            The sequence of profiles to be used
        tol: float, optional
            tolerance for profile's C2 conversion (default: {1e-6})
        build_solid: bool, optional
            Toggle solid construction (default: {False})
        use_smoothing: bool, optional
            Builds a C2 smoothed approximation of profiles (default: {False})
        w: Tuple(floa)t, optional
            smoothing weight on curve length, curvature and torsion (default: {1., 1., 1.})
        max_deg: int, optional
            max bspline deggreee for approx (default: {8})

        Returns
        -------
        sh: TopoDS_Shape
            Lofted shell or solid
        """
        from pyoccad.create import CreateWire

        is_ruled = len(profile_lst) == 2
        ThruSections = BRepOffsetAPI_ThruSections(build_solid, is_ruled, tol)
        ThruSections.SetSmoothing(use_smoothing)
        ThruSections.SetCriteriumWeight(*w)
        ThruSections.SetMaxDegree(max_deg)

        for profile in profile_lst:
            Profile = CreateWire.from_element(profile)
            ThruSections.AddWire(Profile)

        return ThruSections.Shape()
