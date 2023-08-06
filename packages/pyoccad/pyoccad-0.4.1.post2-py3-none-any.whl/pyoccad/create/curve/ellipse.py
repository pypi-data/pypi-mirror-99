from typing import Tuple

import numpy as np
from OCC.Core.GC import GC_MakeEllipse
from OCC.Core.Geom import Geom_Ellipse
from OCC.Core.gp import gp_Ax2

from pyoccad.typing import DirectionT, PointT

FULL_ELLIPSE = 2. * np.pi


class CreateEllipse:
    """Factory to create an ellipse curve."""

    @staticmethod
    def from_center_directions_radii(center: PointT,
                                     directions: Tuple[DirectionT, DirectionT],
                                     radii: Tuple[float, float]) -> Geom_Ellipse:
        """Create an ellipse from its center, normale direction and radii.

        Parameters
        ----------
        center: PointT
            The ellipse center
        directions: Tuple[DirectionT, DirectionT]
            The normale and major axis directions
        radii: Tuple[float, float]
            The minor and major radius

        Returns
        -------
        ellipse: Geom_Ellipse
            The resulting ellipse
        """
        normale_direction, major_radius_direction = directions
        minor_radius, major_radius = radii
        ellipse = GC_MakeEllipse(gp_Ax2(center, normale_direction, major_radius_direction),
                                 major_radius, minor_radius).Value()
        return ellipse
