from math import pi

import numpy as np
from OCC.Core.TopoDS import TopoDS_Vertex
from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Dir, gp_Vec, gp_Ax2, gp_Pnt2d, gp_XY, gp_Ax22d, gp_Dir2d, gp_Vec2d

from pyoccad.create import (CreateUnsignedCoordSystem, CreateCoordSystem, CreateBezier, CreatePoint, CreatePlane,
                            CreateTopology)
from pyoccad.tests.testcase import TestCase


class CreatePointTest(TestCase):

    def __test_constructor(self, f, p_2d, p_3d):
        x = (1, 2, 3)
        self.assertAlmostSameCoord(p_3d, f(gp_Pnt(*x)))
        self.assertAlmostSameCoord(p_3d, f(gp_XYZ(*x)))
        self.assertAlmostSameCoord(p_3d, f(gp_Vec(*x)))
        self.assertAlmostSameCoord(p_3d, f(list(x)))
        self.assertAlmostSameCoord(p_3d, f(np.array(x)))

        x = (1, 2)
        self.assertAlmostSameCoord(p_2d, f(gp_Pnt2d(*x)))
        self.assertAlmostSameCoord(p_2d, f(gp_XY(*x)))
        self.assertAlmostSameCoord(p_2d, f(gp_Vec2d(*x)))
        self.assertAlmostSameCoord(p_2d, f(list(x)))
        self.assertAlmostSameCoord(p_2d, f(np.array(x)))

        # Tuple of point(s)
        with self.assertRaises(TypeError):
            f((gp_XY(2, 3),))

        # Wrong lengths
        with self.assertRaises(TypeError):
            f((1,))
        with self.assertRaises(TypeError):
            f((1, 2, 3, 4))

        # Wrong types
        with self.assertRaises(TypeError):
            f('a')
        with self.assertRaises(TypeError):
            f(('aa', 'aa'))
        with self.assertRaises(TypeError):
            f(('a', 'b', 'c'))
        with self.assertRaises(TypeError):
            f((1, 'b', 'c'))

    def test_as_point(self):
        p_2d = gp_Pnt2d(1, 2)
        p_3d = gp_Pnt(1, 2, 3)
        self.__test_constructor(CreatePoint.as_point, p_2d, p_3d)

    def test_as_list(self):
        p_2d = [1, 2]
        p_3d = [1, 2, 3]
        self.__test_constructor(CreatePoint.as_list, p_2d, p_3d)

    def test_as_tuple(self):
        p_2d = (1, 2)
        p_3d = (1, 2, 3)
        self.__test_constructor(CreatePoint.as_tuple, p_2d, p_3d)

    def test_as_ndarray(self):
        p_2d = np.r_[1, 2]
        p_3d = np.r_[1, 2, 3]
        self.__test_constructor(CreatePoint.as_ndarray, p_2d, p_3d)

    def test_from_vertex(self):
        pt = CreatePoint.as_point([0, 0, 0])
        vtx = CreateTopology.make_vertex(pt)
        self.assertIsInstance(vtx, TopoDS_Vertex)

        point = CreatePoint.from_vertex(vtx)
        self.assertIsInstance(point, gp_Pnt)
        self.assertAlmostSameCoord(point, pt)

    def test_from_cylindrical(self):
        referential = gp_Ax2(gp_Pnt(), gp_Dir(0, 0, 1))
        x = [1, pi / 2, 2.]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, referential), (0., 1., 2.))
        x = [1, 3 * pi / 2, 2.]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, referential), (0., -1., 2.))
        x = [1, pi, 2.]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, referential), (-1., 0., 2.))
        x = [1, pi, 2.]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, gp_Ax2(gp_Pnt(2., 10., 5.), gp_Dir(0, 0, 1))),
                                   (1., 10., 7.))

        referential = gp_Ax22d(gp_Pnt2d(), gp_Dir2d(0, 1))
        x = [1, pi / 2]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, referential), (-1., 0.))
        x = [1, 3 * pi / 2]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, referential), (1., 0.))
        x = [1, pi]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, referential), (0., -1.))
        x = [1, pi]
        self.assertAlmostSameCoord(CreatePoint.from_cylindrical(x, gp_Ax22d(gp_Pnt2d(2., 10.), gp_Dir2d(0, -1))),
                                   (2., 11.))

        with self.assertRaises(AttributeError):
            CreatePoint.from_cylindrical([1, pi], gp_Ax2(gp_Pnt(), gp_Dir(0, 0, 1)))

        with self.assertRaises(AttributeError):
            CreatePoint.from_cylindrical([1, pi, 10], gp_Ax22d(gp_Pnt2d(2., 10.), gp_Dir2d(0, -1)))

    def test_from_curve(self):
        crv = CreateBezier.from_poles([[0., 0., 0.], [1., 1., 1], [3., 3., 3]])

        self.assertAlmostSameCoord(CreatePoint.from_curve(crv, 0.), gp_Pnt(0., 0., 0.))
        self.assertAlmostSameCoord(CreatePoint.from_curve(crv, 1.), gp_Pnt(3., 3., 3.))
        self.assertAlmostSameCoord(CreatePoint.from_curve(crv, 0.5), gp_Pnt(1.25, 1.25, 1.25))

    def test_centroid(self):
        p1 = CreatePoint.as_point((0, 0, 0))
        p2 = CreatePoint.as_point((1, 0, 0))
        p3 = CreatePoint.centroid((p1, p2))
        self.assertAlmostSameCoord(p3, (0.5, 0, 0))

        p1 = CreatePoint.as_point((0, 0))
        p2 = CreatePoint.as_point((1, 0))
        p3 = CreatePoint.centroid((p1, p2))
        self.assertAlmostSameCoord(p3, (0.5, 0))

    def test_barycenter(self):
        p1 = CreatePoint.as_point((0, 0, 0))
        p2 = CreatePoint.as_point((1, 1, 1))
        p3 = CreatePoint.barycenter((p1, p2), (0.2, 0.8))
        self.assertAlmostSameCoord(p3, (0.8, 0.8, 0.8))

        p1 = CreatePoint.as_point((0, 0))
        p2 = CreatePoint.as_point((1.6, 1.2))
        p3 = CreatePoint.barycenter((p1, p2), (0.5, 0.5))
        self.assertAlmostSameCoord(p3, (0.8, 0.6))

    def test_as_point_in_referential(self):
        ax3 = CreateUnsignedCoordSystem.from_location_and_directions([1, 1, 1], [0, 0, 1], [1, 0, 0])
        p = CreatePoint.as_point_in_referential((1, 2, 3), ax3)
        self.assertAlmostSameCoord(p, (1 + 3, 1 - 2, 1 + 1))

        ax22d = CreateCoordSystem.from_location_and_directions([1, 1], [0, 1], [1, 0])
        p = CreatePoint.as_point_in_referential((1, -5), ax22d)
        self.assertAlmostSameCoord(p, (1 - 5, 1 + 1))

        with self.assertRaises(AttributeError):
            CreatePoint.as_point_in_referential((1, -5), ax3)

    def test_from_curve_relative_pos(self):
        crv = CreateBezier.from_poles([[0., 0., 0.], [1., 1., 1], [3., 3., 3]])

        self.assertAlmostSameCoord(CreatePoint.from_curve_relative_pos(crv, 0.), gp_Pnt(0., 0., 0.))
        self.assertAlmostSameCoord(CreatePoint.from_curve_relative_pos(crv, 1.), gp_Pnt(3., 3., 3.))
        self.assertAlmostSameCoord(CreatePoint.from_curve_relative_pos(crv, 0.5), gp_Pnt(1.5, 1.5, 1.5))

    def test_projected_on_plane(self):
        point = CreatePoint.as_point((10, 10, 10))
        projected_point = CreatePoint.projected_on_plane(point, CreatePlane.xoy())
        self.assertAlmostSameCoord(projected_point, (10, 10, 0))
