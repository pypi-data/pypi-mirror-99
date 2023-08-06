# from unittest import skip
#
# from OCC.Core.gp import (gp_Pnt)
# # from occt_extensions.create.curve.curve_builder import BSplineControlPoint
#
# from pyoccad.create.point import CreatePoint
# from pyoccad.create.container.array import CreateHArray1
# from pyoccad.tests.testcase import TestCase
#
#
# class BSplineControlPointTest(TestCase):
#
#     def setUp(self):
#         self.cp = BSplineControlPoint(CreatePoint.as_point((0., 1., 2.)))
#
#     def test___init__(self):
#         self.assertIsInstance(self.cp, BSplineControlPoint)
#
#     def test_dn(self):
#         self.assertIsInstance(self.cp.DN(0), gp_Pnt)
#
#     def test_dn_constrained(self):
#         self.assertTrue(self.cp.isDNContrained(0))
#         self.assertFalse(self.cp.isDNContrained(1))
#
#
# class BSplineBuilderTest(TestCase):
#
#     @skip('Not ready yet')
#     @staticmethod
#     def test_bspline_builder():
#         from occt_extensions.create.curve import curve_builder
#         builder = curve_builder.bsplineBuilder()
#
#         builder.push_back(gp_Pnt(20, 530, 0))
#         builder.push_back(gp_Pnt(50, 520, 0))
#         builder.push_back(gp_Pnt(70, 530, 0))
#         builder.push_back(gp_Pnt(90, 520, 0))
#
#         builder.curveCheck()
#
#         params = CreateHArray1.of_floats([0., 0.1, 0.6, 1.])
#         builder.setParameters(params)
#
#         builder.curveCheck()
