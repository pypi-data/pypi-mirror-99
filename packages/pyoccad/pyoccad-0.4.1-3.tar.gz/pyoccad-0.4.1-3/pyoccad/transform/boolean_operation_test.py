from pyoccad.create import (CreatePlane, CreateBSpline, CreateBox, CreateFace, CreateRevolution,
                            CreateAxis, CreateTopology)
from pyoccad.explore import ExploreSubshapes
from pyoccad.measure import solid as ms
from pyoccad.measure.surface import MeasureSurface
from pyoccad.measure.curve import MeasureCurve
from pyoccad.tests.testcase import TestCase
from pyoccad.transform import BooleanOperation


class TestBop(TestCase):

    def test_common(self):
        box = CreateBox.from_dimensions_and_center((1., 1., 1.))
        f1 = CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 2, 2)
        f2 = BooleanOperation.common([box], [f1])
        self.assertAlmostEqualValues(MeasureSurface.area(f2), 1.)

    def test_split(self):
        box = CreateBox.from_dimensions_and_center((1., 1., 1.))
        f1 = CreateFace.from_plane_and_sizes(CreatePlane.xoy(), 2, 2)
        split = BooleanOperation.split([box], [f1])
        self.assertEqual(len(ExploreSubshapes.get_solids(split)), 2)
        for s in ExploreSubshapes.get_solids(split):
            self.assertAlmostEqualValues(ms.volume(s), 0.5)

    def test_cut(self):
        box1 = CreateBox.from_dimensions((1, 1, 1))
        box2 = CreateBox.from_dimensions_and_center((0.3, 0.3, 0.3), [0.5, 0.5, 0.])
        cut = BooleanOperation.cut([box1], [box2])
        v1 = ms.volume(box1)
        v2 = ms.volume(box2)
        self.assertAlmostEqualValues(ms.volume(cut), v1 - 0.5 * v2)

    def test_cut_half_space(self):
        box = CreateBox.from_dimensions_and_center((3, 3, 3), [0.5, 0.5, 0.5])
        cut_box = BooleanOperation.cut_half_space([box], CreatePlane.xoy(), True)
        self.assertAlmostEqualValues(27, ms.volume(box))
        self.assertAlmostEqualValues(9, ms.volume(cut_box))

        cut_box = BooleanOperation.cut_half_space([box], CreatePlane.xoy(), False)
        self.assertAlmostEqualValues(18, ms.volume(cut_box))

    def test_fuse(self):
        box1 = CreateBox.from_dimensions((1, 1, 1))
        box2 = CreateBox.from_dimensions_and_center((0.3, 0.3, 0.3), [0.5, 0.5, 0.])
        fuse = BooleanOperation.fuse([box1], [box2])
        v1 = ms.volume(box1)
        v2 = ms.volume(box2)
        self.assertAlmostEqualValues(ms.volume(fuse), v1 + 0.5 * v2)

    def test_fuse_with_fillet(self):
        box1 = CreateBox.from_dimensions((1, 1, 1))
        box2 = CreateBox.from_dimensions_and_center((0.3, 0.3, 0.3), [0.5, 0.5, 0.])
        fuse = BooleanOperation.fuse_with_fillet([box1], [box2], 0.05, )
        v1 = ms.volume(box1)
        v2 = ms.volume(box2)
        self.assertGreater(ms.volume(fuse), v1 + 0.5 * v2)

    def test_section(self):
        box1 = CreateBox.from_dimensions((1, 1, 1))
        box2 = CreateBox.from_dimensions_and_center((0.3, 0.3, 0.3), [0.5, 0.5, 0.])
        fuse = BooleanOperation.fuse([box1], [box2])
        e_lst = ExploreSubshapes.get_edges(BooleanOperation.section([box1], [box2]))
        l = 0.
        for c in e_lst:
            self.assertAlmostEqualValues(MeasureCurve.length(c), 0.3)

    def test_extrude_cut(self):
        c1 = 1.
        x1 = 1.5
        bs = CreateBSpline.from_points_and_tangents_interpolate(
            points=[[x1, 0., 0.], [x1 + 0.44 * c1, 0.05, 0.], [x1 + c1, 0., 0.], [x1 + 0.44 * c1, -0.05, 0.]],
            tangents=[[0, 0.25, 0], [1, 0, 0], [0, -0.1, 0], [-1, 0, 0]],
            tol=1e-6,
            periodic=True,
            directions_only=False
        )

        bs1 = CreateBSpline.from_points_interpolate_with_bounds_control([[0, 0, 0], [3, 1, 0]],
                                                                        ([3, 1, 0], [1, 0, 0]), 1e-6)
        bs2 = CreateBSpline.from_points_interpolate([[0, 2, 0], [1.5, 1.8, 0], [3, 2, 0]], 1e-6)
        rev1 = CreateRevolution.surface_from_curve(bs1, CreateAxis.ox())
        rev2 = CreateRevolution.surface_from_curve(bs2, CreateAxis.ox())

        n_edges1 = len([e for e in ExploreSubshapes.get_edges(CreateTopology.as_shape(rev1))])
        n_edges2 = len([e for e in ExploreSubshapes.get_edges(CreateTopology.as_shape(rev2))])
        n_edges = len([e for e in ExploreSubshapes.get_edges(BooleanOperation.extrude_cut([rev1, rev2],
                                                                                          bs,
                                                                                          [0., 0., 1.]))])

        self.assertEqual(n_edges, n_edges1 + n_edges2 + 2)
