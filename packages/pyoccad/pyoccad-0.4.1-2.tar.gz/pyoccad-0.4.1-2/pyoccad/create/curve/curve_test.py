from OCC.Core.Adaptor2d import Adaptor2d_Curve2d, Adaptor2d_HCurve2d
from OCC.Core.Adaptor3d import Adaptor3d_Curve, Adaptor3d_HCurve
from OCC.Core.BRepAdaptor import BRepAdaptor_HCurve, BRepAdaptor_HCompCurve
from OCC.Core.Geom import Geom_Curve, Geom_TrimmedCurve
from OCC.Core.Geom2d import Geom2d_Curve, Geom2d_Circle
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve, Geom2dAdaptor_HCurve
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve, GeomAdaptor_HCurve
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire

from pyoccad.create import (CreateCircle, CreateCurve, CreateEdge, CreateWire, CreatePlane, CreateCoordSystem,
                            CreateLine, CreateBSpline)
from pyoccad.measure import MeasureCurve
from pyoccad.tests.testcase import TestCase


class CreateCurveTest(TestCase):

    def test_as_curve(self):
        r = 1.

        # Geom
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertIsInstance(CreateCurve.as_curve(c), Geom_Curve)

        # Geom2d
        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertIsInstance(CreateCurve.as_curve(c2d), Geom2d_Curve)

        # Edge
        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(e, TopoDS_Edge)
        self.assertIsInstance(CreateCurve.as_curve(e), TopoDS_Edge)

        # Wire
        w = CreateWire.from_element(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertIsInstance(CreateCurve.as_curve(w), TopoDS_Wire)

        # GeomAdaptor
        a = GeomAdaptor_Curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(a, Adaptor3d_Curve)
        self.assertIsInstance(CreateCurve.as_curve(a), Geom_Curve)

        # Geom2dAdaptor
        a2d = Geom2dAdaptor_Curve(CreateCircle.from_3d(CreateCircle.from_radius_and_center(r)))
        self.assertIsInstance(a2d, Adaptor2d_Curve2d)
        self.assertIsInstance(CreateCurve.as_curve(a2d), Geom2d_Curve)

        # GeomAdaptorHandler
        adaptor_handler = CreateCurve.as_adaptor_handler(c)
        self.assertIsInstance(adaptor_handler, GeomAdaptor_HCurve)
        self.assertIsInstance(CreateCurve.as_curve(adaptor_handler), Geom_Curve)

        # GeomAdaptorHandler
        adaptor2d_handler = CreateCurve.as_adaptor_handler(c2d)
        self.assertIsInstance(adaptor2d_handler, Adaptor2d_HCurve2d)
        self.assertIsInstance(CreateCurve.as_curve(adaptor2d_handler), Geom2d_Curve)

        with self.assertRaises(TypeError):
            CreateCurve.as_curve(True)

    def test_as_adaptor(self):
        r = 1.

        # Geom
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertIsInstance(CreateCurve.as_adaptor(c), Adaptor3d_Curve)

        # Geom2d
        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertIsInstance(CreateCurve.as_adaptor(c2d), Adaptor2d_Curve2d)

        # Edge
        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(e, TopoDS_Edge)
        self.assertIsInstance(CreateCurve.as_adaptor(e), Adaptor3d_Curve)

        # Wire
        w = CreateWire.from_element(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertIsInstance(CreateCurve.as_adaptor(w), Adaptor3d_Curve)

        # GeomAdaptor
        a = GeomAdaptor_Curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(a, Adaptor3d_Curve)
        self.assertIsInstance(CreateCurve.as_adaptor(a), Adaptor3d_Curve)

        # Geom2dAdaptor
        a2d = Geom2dAdaptor_Curve(CreateCircle.from_3d(CreateCircle.from_radius_and_center(r)))
        self.assertIsInstance(a2d, Adaptor2d_Curve2d)
        self.assertIsInstance(CreateCurve.as_adaptor(a2d), Adaptor2d_Curve2d)

        # GeomAdaptorHandler
        adaptor_handler = CreateCurve.as_adaptor_handler(c)
        self.assertIsInstance(adaptor_handler, Adaptor3d_HCurve)
        self.assertIsInstance(CreateCurve.as_adaptor(adaptor_handler), Adaptor3d_Curve)

        # GeomAdaptorHandler
        adaptor2d_handler = CreateCurve.as_adaptor_handler(c2d)
        self.assertIsInstance(adaptor2d_handler, Adaptor2d_HCurve2d)
        self.assertIsInstance(CreateCurve.as_adaptor(adaptor2d_handler), Adaptor2d_Curve2d)

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor(True)

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor('_')

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor(0.1)

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor((0.,))

    def test_as_adaptor_handler(self):
        r = 1.

        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertIsInstance(CreateCurve.as_adaptor_handler(c), GeomAdaptor_HCurve)

        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertIsInstance(CreateCurve.as_adaptor_handler(c2d), Geom2dAdaptor_HCurve)

        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(e, TopoDS_Edge)
        self.assertIsInstance(CreateCurve.as_adaptor_handler(e), BRepAdaptor_HCurve)

        w = CreateWire.from_element(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertIsInstance(CreateCurve.as_adaptor_handler(w), BRepAdaptor_HCompCurve)

        a = GeomAdaptor_Curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(a, Adaptor3d_Curve)
        self.assertIsInstance(CreateCurve.as_adaptor_handler(a), GeomAdaptor_HCurve)

        a2d = Geom2dAdaptor_Curve(CreateCircle.from_3d(CreateCircle.from_radius_and_center(r)))
        self.assertIsInstance(a2d, Adaptor2d_Curve2d)
        self.assertIsInstance(CreateCurve.as_adaptor_handler(a2d), Geom2dAdaptor_HCurve)

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor_handler(True)

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor_handler('_')

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor_handler(0.1)

        with self.assertRaises(TypeError):
            CreateCurve.as_adaptor_handler((0.,))

    def test_from_adaptor(self):
        r = 1.

        # Geom
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)
        self.assertIsInstance(CreateCurve.from_adaptor(CreateCurve.as_adaptor(c)), Geom_Curve)

        # Geom2d
        c2d = CreateCircle.from_3d(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(c2d, Geom2d_Curve)
        self.assertIsInstance(CreateCurve.from_adaptor(CreateCurve.as_adaptor(c2d)), Geom2d_Curve)

        # Edge
        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(e, TopoDS_Edge)
        self.assertIsInstance(CreateCurve.from_adaptor(CreateCurve.as_adaptor(e)), TopoDS_Edge)

        # Wire
        w = CreateWire.from_element(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(w, TopoDS_Wire)
        self.assertIsInstance(CreateCurve.from_adaptor(CreateCurve.as_adaptor(w)), TopoDS_Wire)

        # Wire adaptor handler
        w_adaptor_handler = CreateCurve.as_adaptor_handler(w)
        self.assertIsInstance(w_adaptor_handler, BRepAdaptor_HCompCurve)
        self.assertIsInstance(CreateCurve.from_adaptor(w_adaptor_handler), TopoDS_Wire)

        # GeomAdaptor
        a = GeomAdaptor_Curve(CreateCircle.from_radius_and_center(r))
        self.assertIsInstance(a, Adaptor3d_Curve)
        self.assertIsInstance(CreateCurve.from_adaptor(CreateCurve.as_adaptor(a)), Geom_Curve)

        # Geom2dAdaptor
        a2d = Geom2dAdaptor_Curve(CreateCircle.from_3d(CreateCircle.from_radius_and_center(r)))
        self.assertIsInstance(a2d, Adaptor2d_Curve2d)
        self.assertIsInstance(CreateCurve.from_adaptor(CreateCurve.as_adaptor(a2d)), Geom2d_Curve)

        # GeomAdaptorHandler
        adaptor_handler = CreateCurve.as_adaptor_handler(c)
        self.assertIsInstance(adaptor_handler, Adaptor3d_HCurve)
        self.assertIsInstance(CreateCurve.from_adaptor(adaptor_handler), Geom_Curve)

        # Geom2dAdaptorHandler
        adaptor2d_handler = CreateCurve.as_adaptor_handler(c2d)
        self.assertIsInstance(adaptor2d_handler, Adaptor2d_HCurve2d)
        self.assertIsInstance(CreateCurve.from_adaptor(adaptor2d_handler), Geom2d_Curve)

        with self.assertRaises(TypeError):
            CreateCurve.from_adaptor(True)

        with self.assertRaises(TypeError):
            CreateCurve.from_adaptor('_')

        with self.assertRaises(TypeError):
            CreateCurve.from_adaptor(0.1)

        with self.assertRaises(TypeError):
            CreateCurve.from_adaptor((0.,))

    def test_from_2d(self):
        r = 10.
        c2d = Geom2d_Circle(CreateCoordSystem.from_location_and_directions((0., 0.), (1., 0.), (0., 1.)), r)
        self.assertIsInstance(c2d, Geom2d_Curve)

        plane = CreatePlane.xoy()
        c = CreateCurve.from_2d(c2d, plane)
        self.assertIsInstance(c, Geom_Curve)

    def test_from_3d(self):
        r = 10.
        c = CreateCircle.from_radius_and_center(r)
        self.assertIsInstance(c, Geom_Curve)

        plane = CreatePlane.xoy()
        c2d = CreateCurve.from_3d(c, plane)
        self.assertIsInstance(c2d, Geom2d_Curve)

    def test_from_edge(self):
        bspline = CreateBSpline.from_points(((0., 0., 0.), (1., 2., 3.)))
        e = CreateEdge.from_curve(bspline)
        self.assertIsInstance(e, TopoDS_Edge)

        curve = CreateCurve.from_edge(e)
        self.assertIsInstance(curve, Geom_TrimmedCurve)
        self.assertAlmostSameCoord(curve.StartPoint(), (0., 0., 0.))
        self.assertAlmostSameCoord(curve.EndPoint(), (1., 2., 3.))

    def test_trimmed(self):
        cvr2d = CreateLine.between_2_points([0, 0], [2, 0])
        cvr3d = CreateLine.between_2_points([0, 0, 0], [2, 0, 0])
        trim2d = CreateCurve.trimmed(cvr2d, 0.5, 1.5)
        trim3d = CreateCurve.trimmed(cvr3d, 0.5, 1.5)
        self.assertAlmostEqualValues(MeasureCurve.length(trim2d), 1.)
        self.assertAlmostEqualValues(MeasureCurve.length(trim3d), 1.)

        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(1.))
        with self.assertRaises(TypeError):
            CreateCurve.trimmed(e, 0.5, 1.5)

    def test_curve_with_curvilinear_position(self):
        cvr2d = CreateLine.between_2_points([0, 0], [2, 0])
        cvr3d = CreateLine.between_2_points([0, 0, 0], [2, 0, 0])
        trim2d = CreateCurve.curvilinear_trimmed(cvr2d, 0.25, 0.75)
        trim3d = CreateCurve.curvilinear_trimmed(cvr3d, 0.25, 0.75)
        self.assertAlmostEqualValues(MeasureCurve.length(trim2d), 1.)
        self.assertAlmostEqualValues(MeasureCurve.length(trim3d), 1.)

        e = CreateEdge.from_curve(CreateCircle.from_radius_and_center(1.))
        with self.assertRaises(TypeError):
            CreateCurve.curvilinear_trimmed(e, 0.5, 1.5)
