from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.TopoDS import TopoDS_Vertex

from pyoccad.create import CreatePoint
from pyoccad.typing import PointT


class CreateVertex:
    """Factory to create vertices.

    A vertex is a topological entity that corresponds to a point.

    """
    @staticmethod
    def from_point(point: PointT) -> TopoDS_Vertex:
        """

        Parameters
        ----------
        point

        Returns
        -------

        """
        return BRepBuilderAPI_MakeVertex(CreatePoint.as_point(point)).Vertex()
