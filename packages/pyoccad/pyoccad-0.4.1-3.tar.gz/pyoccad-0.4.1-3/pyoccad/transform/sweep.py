from collections.abc import Iterable as IterableT
from typing import Union, Sequence, Iterable

from OCC.Core.Adaptor3d import Adaptor3d_Curve
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe, BRepOffsetAPI_MakePipeShell
from OCC.Core.Geom import Geom_Surface
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Wire, TopoDS_Edge, TopoDS_Shape

from pyoccad.typing import CurveT

ProfileT = Union[CurveT, Geom_Surface, TopoDS_Face]


class Sweep:
    """Factory to sweep shapes."""

    @staticmethod
    def profile_along_path(profile: ProfileT,
                           path: Union[CurveT, Iterable[CurveT]]) -> TopoDS_Shape:
        """Sweep a profile along a path.

        Parameters
        ----------
        profile : ProfileT
            The profile to sweep (must not contain solids)
        path : Union[CurveT, Iterable[CurveT]]
            The path for sweeping, the path has to be G1

        Returns
        -------
        shape : TopoDS_Shape
            The resulting shape
        """
        from pyoccad.create import CreateCurve, CreateWire, CreatePlane, CreateFace

        # Build wire's path
        if isinstance(path, IterableT):
            spine = CreateWire.from_elements(path)
        else:
            spine = CreateWire.from_element(path)

        # Turn profile into a TopoDS_Shape (face, wire, edge)
        if isinstance(profile, (Geom_Surface, TopoDS_Face)):
            profile = CreateFace.from_contour(profile)
        else:  # it should be a curve
            profile = CreateCurve.as_curve(profile)

            if isinstance(profile, Geom2d_Curve):
                spine_adaptor = CreateCurve.as_adaptor(spine)
                plane = CreatePlane.normal_to_curve_at_position(spine_adaptor, spine_adaptor.FirstParameter())
                profile = CreateCurve.from_2d(profile, plane)

            profile = CreateWire.from_element(profile)

        return BRepOffsetAPI_MakePipe(spine, profile).Shape()

    @staticmethod
    def profiles_along_path(profiles: Sequence[ProfileT],
                            path: Union[CurveT, Iterable[CurveT]],
                            build_solid=False) -> TopoDS_Shape:
        """Creates a pipe sweeping profiles along path using OCC.Core.BRepOffsetAPI.BRepOffsetAPI_MakePipeShell

        Parameters
        ----------
        profiles : Sequence[ProfileT]
            The profiles to sweep (profiles must be convertible to wire)
        path : Union[CurveT, Iterable[CurveT]]
            The path for sweeping, the path has to be G1
        build_solid : bool, optional
            Whether create a solid {Default=False}

        Returns
        -------
        shape : TopoDS_Shape
            The resulting shape
        """
        from pyoccad.create import CreateCurve, CreatePlane, CreateWire, CreateFace
        from pyoccad.explore import ExploreSubshapes

        # Build wire's path
        if isinstance(path, IterableT):
            spine = CreateWire.from_elements(path)
        else:
            spine = CreateWire.from_element(path)

        builder = BRepOffsetAPI_MakePipeShell(spine)
        for profile in profiles:
            # Turn profile into a TopoDS_Shape (face, wire, edge)
            if isinstance(profile, (Geom_Surface, TopoDS_Face)):
                profile = CreateWire.from_elements([*ExploreSubshapes.get_edges(profile)])
            else:  # it should be a curve
                profile = CreateCurve.as_curve(profile)

                if isinstance(profile, Geom2d_Curve):
                    spine_adaptor = CreateCurve.as_adaptor(spine)
                    plane = CreatePlane.normal_to_curve_at_position(spine_adaptor, spine_adaptor.FirstParameter())
                    profile = CreateCurve.from_2d(profile, plane)

                profile = CreateWire.from_element(profile)

            builder.Add(profile)

        if build_solid:
            builder.Build()
            builder.MakeSolid()

        return builder.Shape()
