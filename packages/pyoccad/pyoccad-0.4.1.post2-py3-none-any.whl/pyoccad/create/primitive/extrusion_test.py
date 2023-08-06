from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_SurfaceOfLinearExtrusion, Geom_RectangularTrimmedSurface
from OCC.Core.Precision import precision
from OCC.Core.TopoDS import TopoDS_Shape

from pyoccad.create import (CreateBezier, CreateBSpline, CreatePlane, CreatePoint, CreateFace, CreateRevolution,
                            CreateAxis)
from pyoccad.create.primitive.extrusion import CreateExtrusion
from pyoccad.measure import MeasureCurve, solid, shape
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class CreateExtrusionTest(TestCase):

    def test_curve(self):
        e = BRepBuilderAPI_MakeEdge(CreatePoint.as_point([0, 0, 0]), CreatePoint.as_point([1, 0, 0])).Edge()
        extr = CreateExtrusion.curve(e, [0, 0, 1], True)
        self.assertTrue(isinstance(extr, TopoDS_Shape))
        self.assertTrue(precision.IsInfinite(MeasureSurface.area(extr)))

        extr = CreateExtrusion.curve(e, [0, 0, 1])
        self.assertAlmostEqualValues(MeasureSurface.area(extr), 1.)

        c = CreateBezier.from_poles([[0, 0, 0], [1, 1, 0], [2, 0, 0]])
        extr = CreateExtrusion.curve(c, [0, 0, 1], True)
        self.assertIsInstance(extr, Geom_RectangularTrimmedSurface)
        self.assertTrue(precision.IsInfinite(MeasureSurface.area(extr)))

        extr = CreateExtrusion.curve(c, [0, 0, 1], True, False)
        self.assertIsInstance(extr, Geom_SurfaceOfLinearExtrusion)
        self.assertTrue(precision.IsInfinite(MeasureSurface.area(extr)))

        extr = CreateExtrusion.curve(c, [0, 0, 1])
        self.assertAlmostEqualValues(MeasureSurface.area(extr), MeasureCurve.length(c))

        c = CreateBezier.from_poles([[0, 0], [1, 1], [2, 0]])
        extr = CreateExtrusion.curve(c, [0, 1, 0])
        self.assertAlmostEqualValues(MeasureSurface.area(extr), MeasureCurve.length(c))

    def test_face(self):
        f = CreateFace.from_points([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
        s = CreateExtrusion.surface(f, [0, 0, 1])
        self.assertAlmostEqualValues(solid.volume(s), 1.)
        self.assertAlmostEqualValues(MeasureSurface.area(s), 6.)

    def test_surface_from_to(self):
        bs1 = CreateBSpline.from_points_interpolate_with_bounds_control([[0, 0, 0], [3, 1, 0]],
                                                                        ([3, 1, 0], [1, 0, 0]), 1e-6)
        bs2 = CreateBSpline.from_points_interpolate([[0, 2, 0], [1.5, 1.8, 0], [3, 2, 0]], 1e-6)
        rev1 = CreateRevolution.surface_from_curve(bs1, CreateAxis.ox())
        rev2 = CreateRevolution.surface_from_curve(bs2, CreateAxis.ox())

        f1 = CreateFace.from_plane_and_sizes(CreatePlane.xpy([2, 0, -0.5]), 1., 0.2)
        extr1 = CreateExtrusion.surface_from_to(f1, [0, 0, 1], rev1, rev2)
        self.assertAlmostNullValue(shape.distance(extr1, rev1))
        self.assertAlmostNullValue(shape.distance(extr1, rev2))

        f1 = CreateFace.from_plane_and_sizes(CreatePlane.xpy([2, 0, 0.]), 1., 0.2)
        extr1 = CreateExtrusion.surface_from_to(f1, [0, 0, 1], rev1, rev2)
        self.assertAlmostNullValue(shape.distance(extr1, rev1))
        self.assertAlmostNullValue(shape.distance(extr1, rev2))

        f1 = CreateFace.from_plane_and_sizes(CreatePlane.xpy([2, 0, 0.5]), 1., 0.2)
        extr1 = CreateExtrusion.surface_from_to(f1, [0, 0, 1], rev1, rev2)
        self.assertAlmostNullValue(shape.distance(extr1, rev1))
        self.assertAlmostNullValue(shape.distance(extr1, rev2))

        f1 = CreateFace.from_plane_and_sizes(CreatePlane.xpy([2, 0, 1.5]), 1., 0.2)
        extr1 = CreateExtrusion.surface_from_to(f1, [0, 0, 1], rev1, rev2)
        self.assertAlmostNullValue(shape.distance(extr1, rev1))
        self.assertAlmostNullValue(shape.distance(extr1, rev2))
