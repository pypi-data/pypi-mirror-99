from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.TopoDS import TopoDS_Wire, TopoDS_Face

from pyoccad.create import CreateBezier, CreateOffset, CreateFace
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class CreateOffsetTest(TestCase):

    def test_wire_from_curve(self):
        c = CreateBezier.from_poles([[0, 0, 0], [1, 0, 0]])
        w = CreateOffset.wire_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Wire))
        self.assertAlmostEqualValues(MeasureSurface.area(CreateFace.from_contour(w)), 0.1)

        c = BRepBuilderAPI_MakeEdge(c).Edge()
        with self.assertRaises(Exception):
            w = CreateOffset.wire_from_curve(c, 0.1, [0, 0, 1])

        c = BRepBuilderAPI_MakeWire(c).Wire()
        with self.assertRaises(Exception):
            w = CreateOffset.wire_from_curve(c, 0.1, [0, 0, 1])

        # Trying with finite curvature
        c = CreateBezier.from_poles([[0, 0, 0], [1, 0, 0], [1, 1, 0]])
        w = CreateOffset.wire_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Wire))

        c = BRepBuilderAPI_MakeEdge(c).Edge()
        w = CreateOffset.wire_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Wire))

        c = BRepBuilderAPI_MakeWire(c).Wire()
        w = CreateOffset.wire_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Wire))

    def test_face_from_curve(self):
        c = CreateBezier.from_poles([[0, 0, 0], [1, 0, 0]])
        w = CreateOffset.face_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Face))
        self.assertAlmostEqualValues(MeasureSurface.area(w), 0.1)

        c = BRepBuilderAPI_MakeEdge(c).Edge()
        with self.assertRaises(Exception):
            w = CreateOffset.face_from_curve(c, 0.1, [0, 0, 1])

        c = BRepBuilderAPI_MakeWire(c).Wire()
        with self.assertRaises(Exception):
            w = CreateOffset.face_from_curve(c, 0.1, [0, 0, 1])

        # Trying with finite curvature
        c = CreateBezier.from_poles([[0, 0, 0], [1, 0, 0], [1, 1, 0]])
        w = CreateOffset.face_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Face))

        c = BRepBuilderAPI_MakeEdge(c).Edge()
        w = CreateOffset.face_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Face))

        c = BRepBuilderAPI_MakeWire(c).Wire()
        w = CreateOffset.face_from_curve(c, 0.1, [0, 0, 1])
        self.assertTrue(isinstance(w, TopoDS_Face))
