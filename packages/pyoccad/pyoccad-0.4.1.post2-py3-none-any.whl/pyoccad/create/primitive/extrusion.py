from typing import Union

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.Geom import Geom_Curve, Geom_SurfaceOfLinearExtrusion, Geom_RectangularTrimmedSurface
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.GeomAPI import geomapi
from OCC.Core.Precision import precision
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Face, TopoDS_Shape

from pyoccad.create import CreateAxis, CreateCurve, CreateDirection, CreateFace, CreateVector, CreatePlane
from pyoccad.typing import CurveT, VectorT


class CreateExtrusion:

    @staticmethod
    def curve(curve: CurveT, vector: VectorT,
              is_infinite: bool = False, half_infinite: bool = True) -> Union[Geom_SurfaceOfLinearExtrusion,
                                                                              Geom_RectangularTrimmedSurface,
                                                                              TopoDS_Shape]:
        """Create an extrusion of a curve.

        Parameters
        ----------
        curve: CurveT
            The curve
        vector: VectorT
            The extrusion vector
        is_infinite: bool, optional
            Whether to create an infinite extrusion or not {default=False}
        half_infinite: bool, optional
            Whether to create a half-infinite extrusion or not {default=True}, only active if is_infinite is True

        Returns
        -------
        extrusion: Union[Geom_SurfaceOfLinearExtrusion, Geom_RectangularTrimmedSurface, TopoDS_Shape]
            The resulting extrusion
        """
        curve = CreateCurve.as_curve(curve)
        vector = CreateVector.as_vector(vector)
        direction = CreateDirection.as_direction(vector)

        if isinstance(curve, Geom_Curve):
            extrusion = Geom_SurfaceOfLinearExtrusion(curve, direction)
            u1, u2, v1, v2 = extrusion.Bounds()
            if is_infinite:
                if half_infinite:
                    return Geom_RectangularTrimmedSurface(extrusion, u1, u2, 0, precision.Infinite())
                else:
                    return extrusion
            else:
                return Geom_RectangularTrimmedSurface(extrusion, u1, u2, 0, vector.Magnitude())

        if isinstance(curve, Geom2d_Curve):
            plane = CreatePlane.from_axis(CreateAxis.from_location_and_direction((0, 0, 0), direction))
            curve3d = Geom_Curve.DownCast(geomapi.To3d(curve, plane))
            return CreateExtrusion.curve(curve3d, vector, is_infinite, half_infinite)

        if isinstance(curve, (TopoDS_Edge, TopoDS_Wire)):
            if is_infinite:
                return BRepPrimAPI_MakePrism(curve, direction, not half_infinite).Shape()
            else:
                return BRepPrimAPI_MakePrism(curve, vector).Shape()

    @staticmethod
    def surface(surface, vector: VectorT,
                tol: float = precision.Confusion(),
                is_infinite: bool = False, half_infinite: bool = True) -> TopoDS_Shape:
        """Create an extrusion of a surface.

        Parameters
        ----------
        surface: {Geom_Surface, TopoDS_Wire, TopoDS_Edge, Geom_Cuve,gp_Circ,gp_Elips}
            The surface to extrude
        vector: VectorT
            The extrusion vector
        tol: float, optional
            Tolerance value for the resolution of degenerated edges {default=precision.Confusion()}
        is_infinite: bool, optional
            Whether to create an infinite extrusion or not {default=False}
        half_infinite: bool, optional
            Whether to create a half-infinite extrusion or not {default=True}, only active if is_infinite is True

        Returns
        -------
        s: TopoDS_Shape
            The resulting extrusion
        """

        if isinstance(surface, TopoDS_Face):
            f = surface
        else:
            f = CreateFace.from_contour(surface)

        if is_infinite:
            return BRepPrimAPI_MakePrism(f, CreateDirection.as_direction(vector), not half_infinite).Shape()
        else:
            return BRepPrimAPI_MakePrism(f, CreateVector.from_point(vector)).Shape()

    @staticmethod
    def surface_from_to(srf, v, sh_start, sh_end, TolDegen=precision.Confusion()):
        """Extrude a face/surface from sh_start to sh_end

        Parameters
        ----------
        srf : {Geom_Surface, TopoDS_Wire, TopoDS_Edge, Geom_Cuve,gp_Circ,gp_Elips}
            the contour to extrude
        v : Container of coordinates
            Extrusion direction
        sh_start : TopoDS_Shape
            Extrusion start
        sh_end : TopoDS_Shape
            Extrusion end
        TolDegen : float, optional
            tolerance value for resolution of degenerated edges (default: {precision.Confusion()})

        Raises
        ------
        RuntimeError
            If Fails

        Returns
        -------
        s : TopoDS_Shape
            The extruded solid

        """
        from pyoccad.transform import BooleanOperation
        from pyoccad.explore.subshapes import ExploreSubshapes
        from pyoccad.measure import shape

        half_infinite_extrusion = CreateExtrusion.surface(
            srf, v, is_infinite=True, tol=TolDegen)
        split1 = BooleanOperation.split([half_infinite_extrusion], [sh_start, sh_end])

        solid_lst = ExploreSubshapes.get_solids(split1)

        extr = None
        d3_min = precision.Infinite()
        for sol in solid_lst:
            d1 = shape.distance(sol, sh_start)
            d2 = shape.distance(sol, sh_end)
            d3 = shape.distance(sol, srf)
            if d1 < 1e-6 and d2 < 1e-6:
                if d3 < d3_min:
                    d3_min = d3
                    extr = sol

        if extr is not None:
            return extr
        else:
            half_infinite_extrusion = CreateExtrusion.surface(
                srf, v, is_infinite=True, tol=TolDegen, half_infinite=False)
            split1 = BooleanOperation.split([half_infinite_extrusion], [sh_start, sh_end])

            solid_lst = ExploreSubshapes.get_solids(split1)

            extr = None
            d3_min = precision.Infinite()
            for sol in solid_lst:
                d1 = shape.distance(sol, sh_start)
                d2 = shape.distance(sol, sh_end)
                d3 = shape.distance(sol, srf)
                if d1 < 1e-6 and d2 < 1e-6:
                    if d3 < d3_min:
                        d3_min = d3
                        extr = sol
            if extr is not None:
                return extr
            else:
                raise RuntimeError  # if nothing found

    # @staticmethod
    # # TODO: finish the job or delete this method
    # def curve_from_to(crv, d, sh_start, sh_end):
    #     # DO NOT USE
    #     raise NotImplementedError
    #     d_extr = CreateDirection.as_direction(d)
    #     vec = vector.from_point(d_extr).Scaled(1.2 * shape.encompasing_sphere_diameter([sh_end, sh_start, crv]))
    #     half_infinite_extrusion = curve(crv, vec, is_infinite=False)
    #
    #     half_infinite_extrusion = boolean_operation.common([solid.box_bounding_shape_list([sh_start, sh_end])], [half_infinite_extrusion])
    #     split1 = boolean_operation.split([half_infinite_extrusion], [sh_start, sh_end])
    #
    #     face_lst = ExploreSubshapes.get_faces(split1)
    #
    #     Sewing = BRepBuilderAPI_Sewing()
    #
    #     for fa in face_lst:
    #         d1 = shape.distance(fa, sh_start)
    #         d2 = shape.distance(fa, sh_end)
    #         if d1 < 1e-6 and d2 < 1e-6:
    #             Sewing.Add(fa)
    #     Sewing.Perform()
    #     return Sewing.SewedShape()
