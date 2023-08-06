import os

from pyoccad.create import CreateLine, CreateSphere, CreateBox
from pyoccad.exchange import cad
from pyoccad.tests.testcase import TestCase


class TestCAD(TestCase):

    def test_to_iges(self):
        sph = CreateSphere.from_radius_and_center(1.)  # Todo check why iges export box bails-> possible occt issue
        seg = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        self.assertTrue(cad.to_iges([sph, seg], "test_to_iges"))

        if os.path.exists("test_to_iges.igs"):
            os.remove("test_to_iges.igs")

    def test_to_step(self):
        box = CreateBox.from_dimensions((1, 1, 1))
        seg = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        self.assertTrue(cad.to_step([box, ], "test_to_step"))

        if os.path.exists("test_to_step.stp"):
            os.remove("test_to_step.stp")

        with self.assertRaises(TypeError):
            self.assertTrue(cad.to_step([box, seg], "test_to_step"))
