from math import pi

from OCC.Core.Geom import Geom_RectangularTrimmedSurface, Geom_SurfaceOfRevolution
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Solid

from pyoccad.create import (CreateAxis, CreateBezier, CreateEdge, CreateRevolution, CreateWire, CreateFace, CreatePoint,
                            CreateCircle, CreateCurve)
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class CreateRevolutionTest(TestCase):

    def setUp(self):
        self.axis = CreateAxis.oz()

    def test_surface_from_curve(self):
        r = 1.
        l = 2.

        # 3D curve
        crv = CreateBezier.from_poles([[0, r, 0], [0, r, l]])
        rev = CreateRevolution.surface_from_curve(crv, self.axis)
        self.assertIsInstance(rev, Geom_SurfaceOfRevolution)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l)

        # 2D curve
        crv2d = CreateBezier.from_poles([[0, r], [l, r]])
        rev = CreateRevolution.surface_from_curve(crv2d, self.axis)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l)

        # Edge
        ed = CreateEdge.from_contour(crv)
        rev = CreateRevolution.surface_from_curve(ed, self.axis)
        self.assertIsInstance(rev, TopoDS_Shape)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l)

        # 3D curve adaptor
        curve_adaptor = CreateCurve.as_adaptor(crv)
        rev = CreateRevolution.surface_from_curve(curve_adaptor, self.axis)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l)

        with self.assertRaises(TypeError):
            CreateRevolution.surface_from_curve(crv, CreateAxis.from_location_and_direction((0., 0.), (0., 1.)))

        with self.assertRaises(TypeError):
            CreateRevolution.surface_from_curve(CreatePoint.as_point((0., 0., 0.)), CreateAxis.oy())

    def test_trimmed_surface_from_curve(self):
        r = 1.
        l = 2.
        crv = CreateBezier.from_poles([[0, r, 0], [0, r, l]])
        rev = CreateRevolution.trimmed_surface_from_curve(crv, self.axis, 0, pi / 4)
        self.assertIsInstance(rev, Geom_RectangularTrimmedSurface)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l / 8)

        crv2d = CreateBezier.from_poles([[0, r], [l, r]])
        rev = CreateRevolution.trimmed_surface_from_curve(crv2d, self.axis, 0, pi / 4)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l / 8)

        ed = CreateEdge.from_contour(crv)
        with self.assertRaises(TypeError):
            CreateRevolution.trimmed_surface_from_curve(ed, self.axis, 0, pi / 4)

    def test_solid_from_curve(self):
        r = 1.
        l = 2.
        curve = CreateWire.from_points(((0., 0., 0.),
                                        (r, 0., 0.),
                                        (r, l, 0.),
                                        (0., l, 0.)), auto_close=True)
        rev = CreateRevolution.solid_from_curve(curve,  CreateAxis.oy())
        self.assertIsInstance(rev, TopoDS_Solid)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l + 2 * pi * r**2)

        circle = CreateCircle.from_radius_and_center(1, (2, 0, 0), (0, 0, 1))
        edge = CreateEdge.from_curve(circle)
        rev = CreateRevolution.solid_from_curve(edge, CreateAxis.oy())
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 8 * pi**2)  # Torus surface area

        rev = CreateRevolution.solid_from_curve(circle, CreateAxis.oy())
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 8 * pi**2)  # Torus surface area

        curve_adaptor = CreateCurve.as_adaptor(circle)
        rev = CreateRevolution.solid_from_curve(curve_adaptor, CreateAxis.oy())
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 8 * pi**2)  # Torus surface area

        circle2d = CreateCircle.from_radius_and_center(1, (2, 0), (0, 1))
        rev = CreateRevolution.solid_from_curve(circle2d, CreateAxis.oy())
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 8 * pi**2)  # Torus surface area

        with self.assertRaises(TypeError):
            CreateRevolution.solid_from_curve(curve, CreateAxis.from_location_and_direction((0., 0.), (0., 1.)))

        with self.assertRaises(TypeError):
            CreateRevolution.solid_from_curve(CreatePoint.as_point((0., 0., 0.)), CreateAxis.oy())

    def test_solid_from_face(self):
        r = 1.
        l = 2.
        face = CreateFace.from_points(((0., 0., 0.),
                                       (r, 0., 0.),
                                       (r, l, 0.),
                                       (0., l, 0.)))

        rev = CreateRevolution.solid_from_face(face,  CreateAxis.oy())
        self.assertIsInstance(rev, TopoDS_Solid)
        self.assertAlmostEqualValues(MeasureSurface.area(rev), 2 * pi * r * l + 2 * pi * r**2)

        with self.assertRaises(TypeError):
            CreateRevolution.solid_from_face(face, CreateAxis.from_location_and_direction((0., 0.), (0., 1.)))

        with self.assertRaises(TypeError):
            CreateRevolution.solid_from_face(CreatePoint.as_point((0., 0., 0.)), CreateAxis.oy())
