from typing import Iterable

from OCC.Core.TopTools import TopTools_ListOfShape, TopTools_ListIteratorOfListOfShape
from pyoccad.create import CreateTopology


class CreateOCCList:
    """Factory to create OCC lists."""

    @staticmethod
    def of_shapes(shapes: Iterable) -> TopTools_ListOfShape:
        """Create an OCC list of shapes from a Python container of shapes.

        Parameters
        ----------
        shapes : iterable
            An iterable container of TopoDS_Shape convertible objects

        Returns
        -------
        list_ : TopTools_ListOfShape
        """
        list_ = TopTools_ListOfShape()
        for sh in shapes:
            list_.Append(CreateTopology.as_shape(sh))
        return list_


class CreateList:
    """Factory to create Python lists."""

    @staticmethod
    def from_occ_list(shapes_container: TopTools_ListOfShape) -> list:
        """Create a Python list of shapes from an OpenCascade list of shapes.

        Parameters
        ----------
        shapes_container : TopTools_ListOfShape

        Returns
        -------
        list_ : list[shapes]
        """
        list_ = []
        it = TopTools_ListIteratorOfListOfShape(shapes_container)
        while it.More():
            list_.append(it.Value())
            it.Next()
        return list_
