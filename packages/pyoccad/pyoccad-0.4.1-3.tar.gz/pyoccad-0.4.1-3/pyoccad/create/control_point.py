from OCC.Core.Precision import precision
from OCC.Core.gp import gp_Pnt, gp_Dir

from pyoccad.create import CreatePoint, CreateVector
from pyoccad.typing import PointT, VectorT


class ControlPoint(gp_Pnt):
    """A control point with optional first and second derivatives control

    Notes
    -----
    If the control point derivatives are Null, they are not used.

    Parameters
    ----------
    x: {container of coordinates}, optional
        the point. Defaut value: origin
    d1: {container of coordinates}
        the first derivative vector. Defaut value: Null vector
    d2: {container of coordinates}
        the second derivative vector. Defaut value: Null vector
    """

    def __init__(self, x=(0, 0, 0), d1=(0, 0, 0), d2=(0, 0, 0)):
        gp_Pnt.__init__(self)
        self.SetCoord(*CreatePoint.as_tuple(x))
        self.__d1 = CreateVector.from_point(d1)
        self.__d2 = CreateVector.from_point(d2)

    @property
    def d1(self):
        return self.__d1

    @property
    def d2(self):
        return self.__d2

    @property
    def has_d1(self):
        return self.d1.Magnitude() > precision.Approximation()

    @property
    def has_d2(self):
        return self.d2.Magnitude() > precision.Approximation()

    @property
    def d1_dir(self):
        """Returns the tangent direction

        Returns
        -------
        d: gp_Dir
            the tangent vector direction
        """
        return gp_Dir(self.d1)

    @d1.setter
    def d1(self, t):
        """Sets the tangent vector

        Parameters
        ----------
        t: {container of coordinates}
            the tangent vector
        """
        from pyoccad.measure.vector import MeasureVector

        if MeasureVector.dimension(t) != 3:
            raise AttributeError('Derivative vector should have the same dimension as the point, got dimension {} '
                                 'while point has dimension {}'.format(MeasureVector.dimension(t), 3))
        self.__d1 = CreateVector.from_point(t)

    @property
    def d2_dir(self):
        """Returns the tangent direction

        Returns
        -------
        d: gp_Dir
            the tangent vector direction
        """
        return gp_Dir(self.d2)

    @d2.setter
    def d2(self, t):
        """Sets the tangent vector

        Parameters
        ----------
        t: {container of coordinates}
            the tangent vector
        """
        from pyoccad.measure.vector import MeasureVector

        if MeasureVector.dimension(t) != 3:
            raise AttributeError('Derivative vector should have the same dimension as the point, got dimension {} '
                                 'while point has dimension {}'.format(MeasureVector.dimension(t), 3))
        self.__d2 = CreateVector.from_point(t)


class CreateControlPoint:

    @staticmethod
    def from_point(point: PointT = (0., 0., 0.),
                   d1: VectorT = (0., 0., 0.),
                   d2: VectorT = (0., 0., 0.)) -> ControlPoint:
        return ControlPoint(CreatePoint.as_point(point),
                            CreateVector.as_vector(d1),
                            CreateVector.as_vector(d2))
