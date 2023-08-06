from OCC.Core.Geom import Geom_BezierSurface

from pyoccad.create.container.array import CreateArray2


class CreateBezierSurface:
    """Factory to create Bezier surface.

    As with the Bezier curve, a Bezier surface is defined by a set of control points.

    Similar to interpolation in many respects, a key difference is that the surface does not, in general,
    pass through the central control points; rather, it is "stretched" toward them as though each were an attractive
    force.

    """
    @staticmethod
    def from_poles(poles):
        """Create a bezier surface from poles.

        Parameters
        ----------
        poles: container of coordinates
            The poles

        Returns
        -------
        s: Geom_BezierSurface
            The resulting bezier curve
        """
        poles_ = CreateArray2.of_points(poles)
        return Geom_BezierSurface(poles_)

    @staticmethod
    def from_poles_and_weights(poles, weights):
        """Create a bezier surface from poles and weights.

        Notes
        -----
        cast exception if poles are incorrect

        Parameters
        ----------
        poles: container of coordinates
            The poles
        weights: container of float
            The weights

        Returns
        -------
        s: Geom_BezierSurface
            The resulting bezier curve
        """
        poles_ = CreateArray2.of_points(poles)
        weights_ = CreateArray2.of_floats(weights)
        return Geom_BezierSurface(poles_, weights_)
