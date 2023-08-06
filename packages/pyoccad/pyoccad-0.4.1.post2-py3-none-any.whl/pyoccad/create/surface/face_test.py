from math import pi

from pyoccad.create import CreateCircle, CreateWire, CreatePlane, CreateBox, CreateBezierSurface, CreateFace
from pyoccad.measure.surface import MeasureSurface
from pyoccad.tests.testcase import TestCase


class CreateFaceTest(TestCase):

    def test_from_contour(self):
        circ = CreateCircle.from_radius_and_center(1.)

        f = CreateFace.from_contour(circ)
        self.assertAlmostEqualValues(MeasureSurface.area(f), pi)

        s = CreateBezierSurface.from_poles([
            [[0, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [1, 1, 0]]
        ])
        f = CreateFace.from_contour(s)
        self.assertAlmostEqualValues(MeasureSurface.area(f), 1.)

        w = CreateWire.from_points([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
        f = CreateFace.from_contour(w)
        self.assertAlmostEqualValues(MeasureSurface.area(f), 1.)

    def test_from_points(self):
        f = CreateFace.from_points([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
        self.assertAlmostEqualValues(MeasureSurface.area(f), 1.)

    def test_from_plane_and_sizes(self):
        f = CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 1, 1)
        self.assertAlmostEqualValues(MeasureSurface.area(f), 1.)

    def test_from_plane_and_shape_sizes(self):
        box = CreateBox.from_dimensions((1, 1, 1))
        f = CreateFace.from_plane_and_shape_sizes(CreatePlane.xoy(), box)
        self.assertAlmostEqualValues(MeasureSurface.area(f), 1.)
