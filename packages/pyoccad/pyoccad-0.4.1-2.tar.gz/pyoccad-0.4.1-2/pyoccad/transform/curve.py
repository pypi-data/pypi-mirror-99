from OCC.Core.Adaptor2d import Adaptor2d_HCurve2d, Adaptor2d_Curve2d
from OCC.Core.Adaptor3d import Adaptor3d_HCurve, Adaptor3d_Curve
from OCC.Core.Geom import Geom_BSplineCurve


class TransformCurve:

    @staticmethod
    def move_point_and_tangent(crv, u, pt, tg, tol, starting_condition, ending_condition):
        from pyoccad.create import CreatePoint, CreateCurve, CreateVector, CreateWire, CreateBSpline
        from pyoccad.measure import MeasureCurve

         # TODO: write doc
         # TODO: understand why some cases return object and others none
        if isinstance(crv, Adaptor3d_HCurve) or isinstance(crv, Adaptor2d_HCurve2d):
            move_point_and_tangent(CreateCurve.as_adaptor(crv), u, pt, tg, tol, starting_condition, ending_condition)
        elif isinstance(crv, Adaptor3d_Curve) or isinstance(crv, Adaptor2d_Curve2d):
            move_point_and_tangent(CreateCurve.as_adaptor(crv), u, pt, tg, tol, starting_condition, ending_condition)
        elif isinstance(crv, Geom_BSplineCurve) or isinstance(crv, Geom_BSplineCurve):
            if crv.Degree() < 3:
                crv.IncreaseDegree(3)
            error_status = crv.MovePointAndTangent(u, CreatePoint.as_point(pt), CreateVector.from_point(tg),
                                                   tol, starting_condition, ending_condition)
            if error_status != 0:
                print("move_point_and_tangent error_status", error_status, "retry with approx", crv.Degree(), crv.NbPoles())
                crv = CreateBSpline.approximation(crv, tol)
                error_status = crv.MovePointAndTangent(u, CreatePoint.as_point(pt), CreateVector.from_point(tg),
                                                       tol, starting_condition, ending_condition)
                if error_status != 0:
                    print("move_point_and_tangent error_status", error_status, "failed with approx", crv.Degree(),
                          crv.NbPoles())
                    u1 = crv.FirstParameter()
                    u2 = crv.LastParameter()
                    if u - u1 < tol or u2 - u < tol:
                        u_split = 0.5 * (u1 + u2)
                    else:
                        u_split = u
                    crv1 = CreateCurve.trimmed(crv, u1, u_split)
                    crv2 = CreateCurve.trimmed(crv, u_split, u2)
                    w = CreateWire.from_elements([crv1, crv2])  # Il faut recalculer le paramètre
                    m = MeasureCurve.fraction_length(crv, u1, u) / MeasureCurve.length(crv)
                    crv = CreateBSpline.approximation(w, tol)
                    u = MeasureCurve.position_from_relative_curvilinear_abs(crv, m)
                    error_status = crv.MovePointAndTangent(u, CreatePoint.as_point(pt), CreateVector.from_point(tg),
                                                           tol, starting_condition, ending_condition)
                    if error_status != 0:
                        print("move_point_and_tangent error_status", error_status, "failed with splited approx",
                              crv.Degree(), crv.NbPoles())

            return crv
        else:
            raise NotImplementedError
