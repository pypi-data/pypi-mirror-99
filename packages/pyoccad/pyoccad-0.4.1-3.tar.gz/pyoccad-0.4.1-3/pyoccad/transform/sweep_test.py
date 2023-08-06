from math import pi, sqrt

import numpy as np

from pyoccad.create import (CreateCircle, CreateLine, CreatePlane, CreateFace, CreateWire, CreateCoordSystem,
                            CreateCurve, CreateArc)
from pyoccad.measure import MeasureCurve, MeasureSurface
from pyoccad.measure import solid as ms
from pyoccad.explore import ExploreSubshapes
from pyoccad.tests.testcase import TestCase
from pyoccad.transform import Sweep, BooleanOperation


class TestSweep(TestCase):

    def test_profile_along_path(self):
        profile1 = CreateCircle.from_radius_and_center(1., [0, 0])
        seg1 = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        sweep1 = Sweep.profile_along_path(profile1, seg1)
        self.assertAlmostEqualValues(MeasureSurface.area(sweep1), 2 * pi)

        profile2 = CreateFace.from_plane_and_sizes(CreatePlane.yoz(), 1, 1)
        sweep2 = Sweep.profile_along_path(profile2, seg1)
        self.assertAlmostEqualValues(MeasureSurface.area(sweep2), 6.)
        self.assertAlmostEqualValues(ms.volume(sweep2), 1.)

    def test_profiles_along_path(self):
        r = 0.2
        profile1 = CreateCircle.from_radius_and_center(r, [0, 0, 0], [1, 0, 0])
        l = pi / 4 * r
        profile2 = CreateWire.from_points([[2 - l, 1.5, -l],
                                           [2 + l, 1.5, -l],
                                           [2 + l, 1.5, l],
                                           [2 - l, 1.5, l]], True)

        segment1 = CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0])
        coord_system1 = CreateCoordSystem.as_coord_system(([1, 1, 0], [0, -1, 0], [0, 0, 1]))
        arc1 = CreateArc.from_angles(coord_system1, 0.5, 0, pi / 2)
        segment2 = CreateLine.between_2_points([1.5, 1, 0], [1.5, 1.5, 0])
        path = [segment1, arc1, segment2]
        sweep = Sweep.profiles_along_path([profile1, profile2], path, build_solid=True)
        self.assertEqual(1, len([*ExploreSubshapes.get_shells(sweep)]))
        self.assertEqual(17, len([*ExploreSubshapes.get_faces(sweep)]))
        self.assertEqual(35, len([*ExploreSubshapes.get_edges(sweep)]))

        def create_common(position):
            spine = CreateWire.from_elements(path)
            spine_adaptor = CreateCurve.as_adaptor(spine)
            u1 = spine_adaptor.FirstParameter()
            u2 = spine_adaptor.LastParameter()
            u = u1 + (u2 - u1) * position
            plane = CreatePlane.normal_to_curve_at_position(spine_adaptor, u)
            face = CreateFace.from_plane_and_shape_sizes(plane, sweep)
            common = BooleanOperation.common((sweep, ), (face, ))
            return common

        for position in (0, 1):
            common = create_common(position)
            self.assertAlmostEqualValues(MeasureSurface.perimeter(common), 2 * pi * r)

        profile2 = CreateFace.from_plane_and_sizes(CreatePlane.yoz(), 1, 1)
        sweep = Sweep.profiles_along_path((profile2, ), segment1)

        self.assertEqual(1, len([*ExploreSubshapes.get_shells(sweep)]))
        self.assertEqual(4, len([*ExploreSubshapes.get_faces(sweep)]))
        self.assertEqual(12, len([*ExploreSubshapes.get_edges(sweep)]))

        profile1 = CreateCircle.from_radius_and_center(1., [0, 0])
        sweep = Sweep.profiles_along_path((profile1, ), segment1)
        self.assertAlmostEqualValues(MeasureSurface.area(sweep), 2 * pi)
        self.assertEqual(1, len([*ExploreSubshapes.get_shells(sweep)]))
        self.assertEqual(1, len([*ExploreSubshapes.get_faces(sweep)]))
        self.assertEqual(3, len([*ExploreSubshapes.get_edges(sweep)]))
