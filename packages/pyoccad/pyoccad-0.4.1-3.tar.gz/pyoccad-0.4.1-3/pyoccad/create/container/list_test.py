from OCC.Core.TopTools import TopTools_ListOfShape

from pyoccad.create import CreateList, CreateOCCList, CreateLine, CreateEdge
from pyoccad.tests.testcase import TestCase


class CreateOCCListTest(TestCase):

    def test_of_shapes(self):
        list_1 = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        list_2 = CreateLine.between_2_points([0, 1, 0], [1, 1, 0])
        occ_list = CreateOCCList.of_shapes([list_1, list_2])
        self.assertIsInstance(occ_list, TopTools_ListOfShape)

        with self.assertRaises(TypeError):
            CreateOCCList.of_shapes([CreateEdge.from_curve(list_1), "p"])
        with self.assertRaises(TypeError):
            CreateOCCList.of_shapes([1])
        with self.assertRaises(TypeError):
            CreateOCCList.of_shapes([1.])
        with self.assertRaises(TypeError):
            CreateOCCList.of_shapes((occ_list,))
        with self.assertRaises(TypeError):
            CreateOCCList.of_shapes("abc")


class CreateListTest(TestCase):

    def test_from_occ_list(self):
        list_1 = CreateLine.between_2_points([0, 0, 0], [1, 0, 0])
        list_2 = CreateLine.between_2_points([0, 1, 0], [1, 1, 0])
        occ_list = CreateOCCList.of_shapes([list_1, list_2])
        py_list = CreateList.from_occ_list(occ_list)

        self.assertIsInstance(py_list, list)
        self.assertEqual(2, len(py_list))

        with self.assertRaises(TypeError):
            CreateList.from_occ_list([1.])
