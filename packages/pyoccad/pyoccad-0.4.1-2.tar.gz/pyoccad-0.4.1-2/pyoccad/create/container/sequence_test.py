"""Test container module """
from OCC.Core.TColGeom import TColGeom_SequenceOfCurve

from pyoccad.create.container.sequence import CreateSequence
from pyoccad.create.curve.line import CreateLine
from pyoccad.tests.testcase import TestCase


class CreateSequenceTest(TestCase):

    def test_of_curve(self):
        l1 = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        l2 = CreateLine.between_2_points([0, 1, 0], [1, 1, 0])
        sequence = CreateSequence.of_curves([l1, l2])
        self.assertIsInstance(sequence, TColGeom_SequenceOfCurve)
        self.assertEqual(sequence.Length(), 2)

        _ = CreateSequence.of_curves((sequence,))

        with self.assertRaises(TypeError):
            CreateSequence.of_curves([l1, "p"])
        with self.assertRaises(TypeError):
            CreateSequence.of_curves([1])
        with self.assertRaises(TypeError):
            CreateSequence.of_curves([1.])
        with self.assertRaises(TypeError):
            CreateSequence.of_curves("abc")
