import numpy as np
from OCC.Core.TColStd import (TColStd_Array1OfInteger, TColStd_Array1OfReal, TColStd_Array1OfBoolean,
                              TColStd_Array2OfInteger, TColStd_Array2OfReal, TColStd_Array2OfBoolean,
                              TColStd_HArray1OfInteger, TColStd_HArray1OfReal, TColStd_HArray1OfBoolean,
                              )
from OCC.Core.TColgp import TColgp_HArray2OfPnt2d
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Vec2d

from pyoccad.create.container.array import CreateArray1, CreateArray2, CreateHArray1
from pyoccad.tests.testcase import TestCase


class CreateArray1Test(TestCase):

    def test_has_strict_positive_length(self):
        self.assertEqual(3, CreateArray1.has_strict_positive_length((0., 3, 5)))
        self.assertEqual(1, CreateArray1.has_strict_positive_length([0]))

        with self.assertRaises(ValueError):
            CreateArray1.has_strict_positive_length([])
        with self.assertRaises(ValueError):
            CreateArray1.has_strict_positive_length(())
        with self.assertRaises(TypeError):
            CreateArray1.has_strict_positive_length(True)

    def test_of_points(self):
        result = CreateArray1.of_points([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1), gp_Pnt)

        result = CreateArray1.of_points([[1, 2], [3, 4]])
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1), gp_Pnt2d)

        result = CreateArray1.of_points(CreateHArray1.of_points([[1, 2, 3], [4, 5, 6]]))
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1), gp_Pnt)

        with self.assertRaises(TypeError):
            CreateArray1.of_points([[1, 2, 3], [4, 5]])
        with self.assertRaises(ValueError):
            CreateArray1.of_points([])
        with self.assertRaises(TypeError):
            CreateArray1.of_points([(1,)])
        with self.assertRaises(TypeError):
            CreateArray1.of_points(["abc"])

    def test_of_vectors(self):
        result = CreateArray1.of_vectors([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1), gp_Vec)

        result = CreateArray1.of_vectors([[1, 2], [3, 4]])
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1), gp_Vec2d)

        result = CreateArray1.of_vectors(CreateHArray1.of_vectors([[1, 2, 3], [4, 5, 6]]))
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1), gp_Vec)

        with self.assertRaises(TypeError):
            CreateArray1.of_vectors([[1, 2, 3], [4, 5]])
        with self.assertRaises(ValueError):
            CreateArray1.of_vectors([])
        with self.assertRaises(TypeError):
            CreateArray1.of_vectors([(1,)])
        with self.assertRaises(TypeError):
            CreateArray1.of_vectors(["abc"])

    def test_of_integers(self):
        int_list = [1, 2, 3, 4, 5]
        arr1 = CreateArray1.of_integers(int_list)
        self.assertEqual(arr1.Length(), len(int_list))
        self.assertIsInstance(arr1, TColStd_Array1OfInteger)
        for i, val in enumerate(int_list):
            self.assertEqual(arr1.Value(i + 1), val)

        with self.assertRaises(ValueError):
            CreateArray1.of_integers([])
        with self.assertRaises(TypeError):
            CreateArray1.of_integers([1, 2, 3, 4.])

    def test_of_floats(self):
        float_list = [1., 2., 3., 4., 5.]
        arr1 = CreateArray1.of_floats(float_list)
        self.assertEqual(arr1.Length(), len(float_list))
        self.assertIsInstance(arr1, TColStd_Array1OfReal)
        for i, val in enumerate(float_list):
            self.assertEqual(arr1.Value(i + 1), val)

        with self.assertRaises(ValueError):
            CreateArray1.of_floats([])

    def test_of_booleans(self):
        bool_list = [True, True, False, True, True]
        arr1 = CreateArray1.of_booleans(bool_list)
        self.assertEqual(arr1.Length(), len(bool_list))
        self.assertIsInstance(arr1, TColStd_Array1OfBoolean)
        for i, val in enumerate(bool_list):
            self.assertEqual(arr1.Value(i + 1), val)

        with self.assertRaises(TypeError):
            CreateArray1.of_booleans([[1, 2, 3], True, False, True, True])
        with self.assertRaises(ValueError):
            CreateArray1.of_booleans([])
        with self.assertRaises(TypeError):
            CreateArray1.of_booleans([0, 1])


class CreateArray2Test(TestCase):

    def test_of_points(self):
        result = CreateArray2.of_points([[[1, 2, 3]],
                                         [[4, 5, 6]]])
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1, 1), gp_Pnt)

        result = CreateArray2.of_points([[[1, 2]],
                                         [[3, 4]]])
        self.assertEqual(result.Length(), 2)
        self.assertIsInstance(result.Value(1, 1), gp_Pnt2d)

        result = CreateArray2.of_points(TColgp_HArray2OfPnt2d(result))
        self.assertIsInstance(result.Value(1, 1), gp_Pnt2d)

        with self.assertRaises(TypeError):
            CreateArray2.of_points([[[1, 2, 3]],
                                    [[4, 5]]])
        with self.assertRaises(ValueError):
            CreateArray2.of_points([])
        with self.assertRaises(TypeError):
            CreateArray2.of_points([[(1,)]])
        with self.assertRaises(TypeError):
            CreateArray2.of_points([["abc"]])

    def test_of_integers(self):
        int_list = [[1, 2, 3, 4, 5], [11, 12, 13, 14, 15]]
        arr = CreateArray2.of_integers(int_list)
        self.assertEqual(arr.Length(), np.size(int_list))
        self.assertIsInstance(arr, TColStd_Array2OfInteger)
        for i, row in enumerate(int_list):
            for j, val in enumerate(row):
                self.assertEqual(arr.Value(i + 1, j + 1), val)

        with self.assertRaises(ValueError):
            CreateArray2.of_integers([[]])
        with self.assertRaises(TypeError):
            CreateArray2.of_integers([[1, 2, 3, 4.]])

    def test_of_floats(self):
        float_list = [[1., 2., 3., 4., 5.], [11., 12., 13., 14., 15.]]
        arr = CreateArray2.of_floats(float_list)
        self.assertEqual(arr.Length(), np.size(float_list))
        self.assertIsInstance(arr, TColStd_Array2OfReal)
        for i, row in enumerate(float_list):
            for j, val in enumerate(row):
                self.assertEqual(arr.Value(i + 1, j + 1), val)

        with self.assertRaises(ValueError):
            CreateArray2.of_floats([[]])

    def test_of_booleans(self):
        bool_list = [[True, True, False, True, True]]
        arr = CreateArray2.of_booleans(bool_list)
        self.assertEqual(arr.Length(), np.size(bool_list))
        self.assertIsInstance(arr, TColStd_Array2OfBoolean)
        for i, row in enumerate(bool_list):
            for j, val in enumerate(row):
                self.assertEqual(arr.Value(i + 1, j + 1), val)

        with self.assertRaises(TypeError):
            CreateArray2.of_booleans([[[1, 2, 3], True, False, True, True]])
        with self.assertRaises(ValueError):
            CreateArray2.of_booleans([[]])
        with self.assertRaises(TypeError):
            CreateArray2.of_booleans([[0, 1]])


class CreateHArray1Test(TestCase):

    def test_of_points(self):
        result = CreateHArray1.of_points([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(result.Array1().Length(), 2)
        self.assertTrue(isinstance(result.Array1().Value(1), gp_Pnt))

        result = CreateHArray1.of_points([[1, 2], [3, 4]])
        self.assertEqual(result.Array1().Length(), 2)
        self.assertTrue(isinstance(result.Array1().Value(1), gp_Pnt2d))

        with self.assertRaises(TypeError):
            CreateHArray1.of_points([[1, 2, 3], [4, 5]])
        with self.assertRaises(ValueError):
            CreateHArray1.of_points([])
        with self.assertRaises(TypeError):
            CreateHArray1.of_points([(1,)])
        with self.assertRaises(TypeError):
            CreateHArray1.of_points(True)

    def test_of_vectors(self):
        result = CreateHArray1.of_vectors([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(result.Array1().Length(), 2)
        self.assertIsInstance(result.Array1().Value(1), gp_Vec)

        result = CreateHArray1.of_vectors([[1, 2], [3, 4]])
        self.assertEqual(result.Array1().Length(), 2)
        self.assertIsInstance(result.Array1().Value(1), gp_Vec2d)

        with self.assertRaises(TypeError):
            CreateHArray1.of_vectors([[1, 2, 3], [4, 5]])
        with self.assertRaises(ValueError):
            CreateHArray1.of_vectors([])
        with self.assertRaises(TypeError):
            CreateHArray1.of_vectors([(1,)])
        with self.assertRaises(TypeError):
            CreateHArray1.of_vectors(["abc"])
        with self.assertRaises(TypeError):
            CreateHArray1.of_vectors(True)

    def test_of_integers(self):
        int_list = [1, 2, 3, 4, 5]
        arr1 = CreateHArray1.of_integers(int_list)
        self.assertEqual(arr1.Array1().Length(), len(int_list))
        self.assertIsInstance(arr1, TColStd_HArray1OfInteger)
        for i, val in enumerate(int_list):
            self.assertEqual(arr1.Array1().Value(i + 1), val)

        with self.assertRaises(ValueError):
            CreateHArray1.of_integers([])
        with self.assertRaises(TypeError):
            CreateHArray1.of_integers([1, 2, 3, 4.])

    def test_of_floats(self):
        float_list = [1., 2., 3., 4., 5.]
        arr1 = CreateHArray1.of_floats(float_list)
        self.assertEqual(arr1.Array1().Length(), len(float_list))
        self.assertIsInstance(arr1, TColStd_HArray1OfReal)
        for i, val in enumerate(float_list):
            self.assertEqual(arr1.Array1().Value(i + 1), val)

        with self.assertRaises(ValueError):
            CreateHArray1.of_floats([])

    def test_of_booleans(self):
        bool_list = [True, True, False, True, True]
        arr1 = CreateHArray1.of_booleans(bool_list)
        self.assertEqual(arr1.Array1().Length(), len(bool_list))
        self.assertIsInstance(arr1, TColStd_HArray1OfBoolean)
        for i, val in enumerate(bool_list):
            self.assertEqual(arr1.Array1().Value(i + 1), val)

        with self.assertRaises(TypeError):
            CreateHArray1.of_booleans([[1, 2, 3], True, False, True, True])
        with self.assertRaises(ValueError):
            CreateHArray1.of_booleans([])
        with self.assertRaises(TypeError):
            CreateHArray1.of_booleans([0, 1])
