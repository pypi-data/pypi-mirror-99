from typing import Sized
from typing import Union, Sequence

from OCC.Core.TColStd import (TColStd_Array1OfReal, TColStd_Array1OfBoolean, TColStd_Array1OfInteger)
from OCC.Core.TColStd import TColStd_Array2OfReal, TColStd_Array2OfBoolean, TColStd_Array2OfInteger
from OCC.Core.TColStd import (TColStd_HArray1OfReal, TColStd_HArray1OfInteger, TColStd_HArray1OfBoolean)
from OCC.Core.TColgp import TColgp_Array2OfPnt, TColgp_Array2OfPnt2d, TColgp_HArray2OfPnt, TColgp_HArray2OfPnt2d
from OCC.Core.TColgp import (TColgp_HArray1OfPnt, TColgp_HArray1OfPnt2d, TColgp_HArray1OfVec, TColgp_HArray1OfVec2d,
                             TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array1OfVec, TColgp_Array1OfVec2d)

from pyoccad.create import CreatePoint, CreateVector


class CreateArray1:
    """Factory to create Array1 OpenCascade container.

    An Array1 is the OpenCascade equivalent of a list. It starts at index 1, not 0 like in Python.
    """

    @staticmethod
    def has_strict_positive_length(container: Sized) -> int:
        """Get the length of a sized container and raise a ValueError if it is empty

        Parameters
        ----------
        container : Sized
            A Python sized container

        Returns
        -------
        n : int
            The length of the container
        """
        if not isinstance(container, Sized):
            raise TypeError('Type "{}" has no __len__ method'.format(type(container)))

        n = len(container)
        if not n:
            raise ValueError("Empty container cannot be proceeded")
        return n

    @staticmethod
    def of_points(container: Union[TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt,
                                   Sequence]) -> Union[TColgp_Array1OfPnt, TColgp_Array1OfPnt2d]:
        """Create a 2D/3D Array1OfPnt OpenCascade container from another container

        Notes
        -----
        The dimension of the points is given by the dimension of the first item in container

        Parameters
        ----------
        container : {TColgp_HArray1OfPnt2d, TColgp_HArray1OfPnt, Sequence}
            Container of containers of coordinates

        Returns
        -------
        array : TColgp_Array1OfPnt or TColgp_Array1OfPnt2d
            OpenCascade Array1 of points

        Raises
        ------
        ValueError
            if container is empty
            if the dimension of the containers of coordinates is not 2 or 3
        """
        from pyoccad.measure import MeasurePoint

        if isinstance(container, (TColgp_HArray1OfPnt, TColgp_HArray1OfPnt2d)):
            return container.Array1()

        n = CreateArray1.has_strict_positive_length(container)
        dim = MeasurePoint.dimension(container[0])
        if dim == 2:
            array = TColgp_Array1OfPnt2d(1, n)
        else:  # dim == 3:
            array = TColgp_Array1OfPnt(1, n)

        for i in range(0, n):
            array.SetValue(i + 1, CreatePoint.as_point(container[i]))
        return array

    @staticmethod
    def of_vectors(container: Union[TColgp_HArray1OfVec2d, TColgp_HArray1OfVec,
                                    Sequence]) -> Union[TColgp_Array1OfVec, TColgp_Array1OfVec2d]:
        """Create a 2D/3D Array1OfVec OpenCascade container from another container

        Notes
        -----
        The dimension of the vectors is given by the dimension of the first item in the container

        Parameters
        ----------
        container : {TColgp_HArray1OfVec2d, TColgp_HArray1OfVec, Sequence}
            Container of containers of coordinates

        Returns
        -------
        array : TColgp_Array1OfVec or TColgp_Array1OfVec2d
            OpenCascade Array1 of vectors
        """
        from pyoccad.measure.vector import MeasureVector

        if isinstance(container, (TColgp_HArray1OfVec, TColgp_HArray1OfVec2d)):
            return container.Array1()

        n = CreateArray1.has_strict_positive_length(container)
        dim = MeasureVector.dimension(container[0])
        if dim == 2:
            array = TColgp_Array1OfVec2d(1, n)
        else:  # dim == 3:
            array = TColgp_Array1OfVec(1, n)

        for i in range(0, n):
            array.SetValue(i + 1, CreateVector.from_point(container[i]))
        return array

    @staticmethod
    def of_floats(container: Sequence) -> TColStd_Array1OfReal:
        """Create an Array1 OpenCascade container of floats from another container

        Parameters
        ----------
        container : Sequence
            Container of numbers

        Returns
        -------
        array : TColStd_Array1OfReal
            OpenCascade Array1 of floats
        """
        n = CreateArray1.has_strict_positive_length(container)
        array = TColStd_Array1OfReal(1, n)
        for i in range(0, n):
            array.SetValue(i + 1, container[i])
        return array

    @staticmethod
    def of_integers(container: Sequence) -> TColStd_Array1OfInteger:
        """Create an Array1 OpenCascade container of integers from another container

        Parameters
        ----------
        container : Sequence
            Container of numbers

        Returns
        -------
        array : TColStd_Array1OfInteger
            OpenCascade Array1 of integers
        """
        n = CreateArray1.has_strict_positive_length(container)
        array = TColStd_Array1OfInteger(1, n)
        for i in range(0, n):
            array.SetValue(i + 1, container[i])
        return array

    @staticmethod
    def of_booleans(container: Sequence) -> TColStd_Array1OfBoolean:
        """Create an Array1 OpenCascade container of booleans from another container

        Parameters
        ----------
        container : Sequence
            Container of booleans

        Returns
        -------
        array : TColStd_Array1OfBoolean
            OpenCascade Array1 of booleans
        """
        n = CreateArray1.has_strict_positive_length(container)
        array = TColStd_Array1OfBoolean(1, n)
        for i in range(0, n):
            array.SetValue(i + 1, container[i])
        return array


class CreateArray2:
    """Factory to create Array2 OpenCascade container.

    An Array2 is the OpenCascade equivalent of a 2D list (nested list). It starts at index (1, 1),
    not (0, 0) like in Python.
    """

    @staticmethod
    def of_points(container: Union[TColgp_HArray2OfPnt2d, TColgp_HArray2OfPnt,
                                   Sequence]) -> Union[TColgp_Array2OfPnt, TColgp_Array2OfPnt2d]:
        """Create a 2D/3D Array2OfPnt OpenCascade container from another container

        Notes
        -----
        The dimension of the points is given by the dimension of the first item in container

        Parameters
        ----------
        container : {TColgp_HArray2OfPnt2d, TColgp_HArray2OfPnt, Sequence}
            Container of containers of coordinates

        Returns
        -------
        array : TColgp_Array2OfPnt or TColgp_Array2OfPnt2d
            OpenCascade Array2 of points
        """
        from pyoccad.measure import MeasurePoint

        if isinstance(container, (TColgp_HArray2OfPnt2d, TColgp_HArray2OfPnt)):
            return container.Array2()

        n = CreateArray1.has_strict_positive_length(container)
        m = CreateArray1.has_strict_positive_length(container[0])
        dim = MeasurePoint.dimension(container[0][0])
        if dim == 2:
            array = TColgp_Array2OfPnt2d(1, n, 1, m)
        else:  # dim == 3:
            array = TColgp_Array2OfPnt(1, n, 1, m)

        for i in range(0, n):
            for j in range(0, m):
                array.SetValue(i + 1, j + 1, CreatePoint.as_point(container[i][j]))
        return array

    @staticmethod
    def of_floats(container: Sequence) -> TColStd_Array2OfReal:
        """Create an Array2 OpenCascade container of floats from another container

        Parameters
        ----------
        container : Sequence
            Container of numbers

        Returns
        -------
        array : TColStd_Array2OfReal
            OpenCascade Array2 of floats
        """
        n = CreateArray1.has_strict_positive_length(container)
        m = CreateArray1.has_strict_positive_length(container[0])
        array = TColStd_Array2OfReal(1, n, 1, m)
        for i in range(0, n):
            for j in range(0, m):
                array.SetValue(i + 1, j + 1, container[i][j])
        return array

    @staticmethod
    def of_integers(container: Sequence) -> TColStd_Array2OfInteger:
        """Create an Array2 OpenCascade container of integers from another container

        Parameters
        ----------
        container : Sequence
            Container of numbers

        Returns
        -------
        array : TColStd_Array2OfInteger
            OpenCascade Array2 of integers
        """
        n = CreateArray1.has_strict_positive_length(container)
        m = CreateArray1.has_strict_positive_length(container[0])
        array = TColStd_Array2OfInteger(1, n, 1, m)
        for i in range(0, n):
            for j in range(0, m):
                array.SetValue(i + 1, j + 1, container[i][j])
        return array

    @staticmethod
    def of_booleans(container: Sequence) -> TColStd_Array2OfBoolean:
        """Create an Array2 OpenCascade container of booleans from another container

        Parameters
        ----------
        container : Sequence
            Container of booleans

        Returns
        -------
        array : TColStd_Array2OfBoolean
            OpenCascade Array2 of booleans

        Raises
        ------
        ValueError
            if the container is empty
            if the type provided is not a boolean

        """
        n = CreateArray1.has_strict_positive_length(container)
        m = CreateArray1.has_strict_positive_length(container[0])
        array = TColStd_Array2OfBoolean(1, n, 1, m)
        for i in range(0, n):
            for j in range(0, m):
                array.SetValue(i + 1, j + 1, container[i][j])
        return array


class CreateHArray1:
    """Factory to create HArray1 OpenCascade container.

    An HArray1 is an OpenCascade reference to an Array1 object. The "H" stands for "Handler" which is the OpenCascade
    implementation of a smart pointer, it is related to the C++ implementation and has no equivalent in Python.
    """

    @staticmethod
    def of_points(container: Union[TColgp_Array1OfPnt2d, TColgp_Array1OfPnt,
                                   Sequence]) -> Union[TColgp_HArray1OfPnt, TColgp_HArray1OfPnt2d]:
        """Create a 2D/3D HArray1OfPnt OpenCascade container from another container

        Notes
        -----
        The dimension of the points is piloted by the dimension of the first item in X

        Parameters
        ----------
        container : {TColgp_Array1OfPnt2d, TColgp_Array1OfPnt, Sequence}
            Container of containers of coordinates
        Returns
        -------
        hArray : TColgp_HArray1OfPnt or TColgp_HArray1OfPnt2d
            OpenCascade HArray1 of points
        """
        if isinstance(container, Sequence):
            container = CreateArray1.of_points(container)

        if isinstance(container, TColgp_Array1OfPnt2d):
            return TColgp_HArray1OfPnt2d(container)
        if isinstance(container, TColgp_Array1OfPnt):
            return TColgp_HArray1OfPnt(container)

        raise TypeError('Expected type one of (TColgp_Array1OfPnt2d, TColgp_Array1OfPnt, Sequence), '
                        'got {}'.format(type(container)))

    @staticmethod
    def of_vectors(container: Union[TColgp_Array1OfVec2d, TColgp_Array1OfVec,
                                    Sequence]) -> Union[TColgp_HArray1OfVec, TColgp_HArray1OfVec2d]:
        """Create a 2D/3D handler of Array1OfVec OpenCascade container from another container

        Notes
        -----
        The dimension of the vectors is given by the dimension of the first item in the container

        Parameters
        ----------
        container : {TColgp_Array1OfVec2d, TColgp_Array1OfVec, Sequence}
            Container of containers of coordinates

        Returns
        -------
        array : TColgp_HArray1OfVec or TColgp_HArray1OfVec2d
            OpenCascade handler of Array1 of vectors
        """
        if isinstance(container, Sequence):
            container = CreateArray1.of_vectors(container)

        if isinstance(container, TColgp_Array1OfVec2d):
            return TColgp_HArray1OfVec2d(container)
        if isinstance(container, TColgp_Array1OfVec):
            return TColgp_HArray1OfVec(container)

        raise TypeError('Expected type one of (TColgp_Array1OfVec2d, TColgp_Array1OfVec, Sequence), '
                        'got {}'.format(type(container)))

    @staticmethod
    def of_floats(container: Sequence) -> TColStd_HArray1OfReal:
        """Create an HArray1 OpenCascade container of floats from another container

        Parameters
        ----------
        container : Sequence
            Container of numbers

        Returns
        -------
        array : TColStd_HArray1OfReal
            OpenCascade HArray1 of floats
        """
        return TColStd_HArray1OfReal(CreateArray1.of_floats(container))

    @staticmethod
    def of_integers(container: Sequence) -> TColStd_HArray1OfInteger:
        """Create an HArray1 OpenCascade container of integers from another container

        Parameters
        ----------
        container : Sequence
            Container of numbers

        Returns
        -------
        array : TColStd_HArray1OfInteger
            OpenCascade HArray1 of integers
        """
        return TColStd_HArray1OfInteger(CreateArray1.of_integers(container))

    @staticmethod
    def of_booleans(container: Sequence) -> TColStd_HArray1OfBoolean:
        """Create an HArray1 OpenCascade container of booleans from another container

        Parameters
        ----------
        container : Sequence
            Container of booleans

        Returns
        -------
        array : TColStd_Array1OfBoolean
            OpenCascade Array1 of booleans
        """
        return TColStd_HArray1OfBoolean(CreateArray1.of_booleans(container))
