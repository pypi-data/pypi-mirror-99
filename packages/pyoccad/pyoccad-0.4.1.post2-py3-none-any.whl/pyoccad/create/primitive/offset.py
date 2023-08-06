from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCC.Core.Geom import Geom_Curve, Geom_OffsetCurve
from OCC.Core.Geom2d import Geom2d_Curve
from OCC.Core.GeomAPI import geomapi
from OCC.Core.GeomAbs import GeomAbs_Arc
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Face
from OCC.Core.gp import gp_Pln, gp_Pnt

from pyoccad.create import CreateCurve, CreateLine, CreateWire, CreateDirection


class CreateOffset:

    @staticmethod
    def wire_from_curve(crv, offset, dn):
        """creates an offset curve to make a closed contour

        Notes
        -----
        Warning:  in case of curves with infinite curvature please use Geom entities and not TopoDS !!!

        Parameters
        ----------
        crv : {Geom_Curve, Geom2d_curve, TopoDS_Edge, TopoDS_Wire, Adaptor2d_Curve2d, Adaptor3d_Curve}
            the curve element to offset
        offset : float
            offset value
        dn : {gp_Dir, triplet}
            normal direction for offset, not used if edge or wire

        Raises
        ------
        Exception
            if the function meets a curvature issue
        RunTimeError
            if anything goes wrong with OCC

        Returns
        -------
        w : TopoDS_Wire
            The closed wire made by crv and its offset
        """
        if isinstance(crv, Geom_Curve):
            normal = CreateDirection.as_direction(dn)
            crv_offset = Geom_OffsetCurve(crv, offset, normal)
            seg_1 = CreateLine.between_2_curves_starts(crv, crv_offset)
            seg_2 = CreateLine.between_2_curves_ends(crv, crv_offset)
            return CreateWire.from_elements([crv, seg_2, crv_offset, seg_1])
        elif isinstance(crv, Geom2d_Curve):
            normal = CreateDirection.as_direction(dn)
            Pln = gp_Pln(gp_Pnt(), normal)
            crv3d = Geom_Curve.DownCast(geomapi.To3d(crv, Pln))
            return CreateOffset.wire_from_curve(crv3d, offset, dn)
        elif isinstance(crv, TopoDS_Edge):
            return CreateOffset.wire_from_curve(BRepBuilderAPI_MakeWire(crv).Wire(), offset, dn)
        elif isinstance(crv, TopoDS_Wire):
            adCrv = CreateCurve.as_adaptor(crv)
            MakeOffset = BRepOffsetAPI_MakeOffset(crv, GeomAbs_Arc, True)
            MakeOffset.Perform(offset)
            if MakeOffset.Shape() is None:
                raise Exception("Please check wire for finite curvature")
            adCrvOffset = CreateCurve.as_adaptor(MakeOffset.Shape())
            # seg_1 = line.between_2_curve_start(adCrv,adCrvOffset)
            # seg_2 = line.between_2_curve_end(adCrv,adCrvOffset)

            # TODO check if the curves are always reversed
            seg_1 = CreateLine.between_2_curves_at_positions(adCrv, adCrvOffset, adCrv.FirstParameter(),
                                                             adCrvOffset.LastParameter())
            seg_2 = CreateLine.between_2_curves_at_positions(adCrv, adCrvOffset, adCrv.LastParameter(),
                                                             adCrvOffset.FirstParameter())
            return CreateWire.from_elements([adCrv, seg_2, adCrvOffset, seg_1])

        else:
            return CreateOffset.wire_from_curve(CreateCurve.from_adaptor(crv), offset, dn)

    @staticmethod
    def face_from_curve(crv, offset, dn):
        """Creates an offset curve to make a face

        Parameters
        ----------
        crv : {Geom_Curve, Geom2d_curve, TopoDS_Edge, TopoDS_Wire, Adaptor2d_Curve2d, Adaptor3d_Curve}
            the curve element to offset
        offset : float
            offse value
        dn : container of coordinates
            normal direction for offset, not used if edge or wire

        Returns
        -------
        f : TopoDS_Face
            The face made by crv and its offset

        """
        w = CreateOffset.wire_from_curve(crv, offset, dn)
        return BRepBuilderAPI_MakeFace(w).Face()
