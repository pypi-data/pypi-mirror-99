from pyoccad.create import CreatePoint, CreateTranslation, CreateRotation, CreateScaling, CreateSymmetry
from pyoccad.tests.testcase import TestCase


class CreateTranslationTest(TestCase):

    def test_from_vector(self):
        trans = CreateTranslation.from_vector([1, 0, 0])
        origin = CreatePoint.as_point([0, 0, 0])
        x = CreatePoint.as_point([1, 0, 0])
        ox = origin.Transformed(trans)
        self.assertAlmostSameCoord(ox, x)


class CreateRotationTest(TestCase):

    def test_rotation(self):
        x = CreatePoint.as_point([1, 0, 0])
        y = CreatePoint.as_point([0, 1, 0])
        z = CreatePoint.as_point([0, 0, 1])

        oy = x.Transformed(CreateRotation.rotation_z_deg(90))
        self.assertAlmostSameCoord(oy, y)

        oz = oy.Transformed(CreateRotation.rotation_x_deg(90))
        self.assertAlmostSameCoord(oz, z)

        oz = x.Transformed(CreateRotation.rotation_y_deg(-90))
        self.assertAlmostSameCoord(oz, z)


class CreateScalingTest(TestCase):

    def test_from_factor_and_center(self):
        x = CreatePoint.as_point([1, 0, 0])
        tx = x.Transformed(CreateScaling.from_factor_and_center(2, (1., 1., 1.)))
        self.assertAlmostSameCoord(tx, (1, -1, -1))

        x2d = CreatePoint.as_point([1, 0])
        tx2d = x2d.Transformed(CreateScaling.from_factor_and_center(2, (1., 1.)))
        self.assertAlmostSameCoord(tx2d, (1, -1))

    def test_from_factor(self):
        x = CreatePoint.as_point([1, 0, 0])

        tx = x.Transformed(CreateScaling.from_factor(2))
        self.assertAlmostSameCoord(tx, (2, 0, 0))

        tx2 = tx.Transformed(CreateScaling.from_factor(2))
        self.assertAlmostSameCoord(tx2, (4, 0, 0))

    def test_from_2d_scale_factor(self):
        x = CreatePoint.as_point([1, 0])

        tx = x.Transformed(CreateScaling.from_2d_scale_factor(2))
        self.assertAlmostSameCoord(tx, (2, 0))

        tx2 = tx.Transformed(CreateScaling.from_2d_scale_factor(2))
        self.assertAlmostSameCoord(tx2, (4, 0))


class CreateSymmetryTest(TestCase):

    def test_from_ox_axis(self):
        x = CreatePoint.as_point((10, 20, 30))

        tx = x.Transformed(CreateSymmetry.from_ox_axis())
        self.assertAlmostSameCoord(tx, (10, -20, -30))

    def test_from_oy_axis(self):
        x = CreatePoint.as_point((10, 20, 30))

        tx = x.Transformed(CreateSymmetry.from_oy_axis())
        self.assertAlmostSameCoord(tx, (-10, 20, -30))

    def test_from_oz_axis(self):
        x = CreatePoint.as_point((10, 20, 30))

        tx = x.Transformed(CreateSymmetry.from_oz_axis())
        self.assertAlmostSameCoord(tx, (-10, -20, 30))
