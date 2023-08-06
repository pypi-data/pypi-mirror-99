from math import radians
from typing import Union

from OCC.Core.gp import gp_Trsf, gp_Trsf2d, gp_Pnt2d, gp_Ax3, gp_Ax1

from pyoccad.create import CreateAxis, CreatePoint, CreateVector
from pyoccad.typing import PointT, VectorT


class CreateTranslation:
    """Factory to create translations."""

    @staticmethod
    def from_vector(vector: VectorT) -> Union[gp_Trsf, gp_Trsf2d]:
        """Build a translation

        Parameters
        ------------
        vector: VectorT
            The translation vector

        Returns
        ---------
        transformation: Union[gp_Trsf, gp_Trsf2d]
            The resulting transformation
        """
        from pyoccad.measure.vector import MeasureVector

        dim = MeasureVector.dimension(vector)
        if dim == 3:
            transformation = gp_Trsf()
        else:  # dim == 2
            transformation = gp_Trsf2d()

        transformation.SetTranslation(CreateVector.from_point(vector))
        return transformation


class CreateRotation:
    """Factory to create rotations."""

    @staticmethod
    def rotation_x(angle, axis: gp_Ax3 = gp_Ax3()) -> gp_Trsf:
        """Build a rotation around x-axis

        Parameters
        ----------
        angle: float
            [rad] Rotation angle
        axis: gp_Ax3, optional
            the geometrical reference, default Oxyz

        Returns
        ---------
        transformation: gp_Trfs
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetRotation(gp_Ax1(axis.Location(), axis.XDirection()), angle)
        return transformation

    @staticmethod
    def rotation_x_deg(angle, axis: gp_Ax3 = gp_Ax3()) -> gp_Trsf:
        """Builds rotation around x-axis

        Parameters
        ------------
        angle: float
            [deg] Rotation angle
        axis: gp_Ax3, optional
            the geometrical reference, default Oxyz

        Returns
        ---------
        transformation: gp_Trfs
            The resulting transformation
        """
        return CreateRotation.rotation_x(radians(angle), axis)

    @staticmethod
    def rotation_y(angle, axis: gp_Ax3 = gp_Ax3()) -> gp_Trsf:
        """Builds rotation around y-axis

        Parameters
        ------------
        angle: float
            [rad] Rotation angle
        axis: gp_Ax3, optional
            the geometrical reference, default Oxyz

        Returns
        ---------
        transformation: gp_Trfs
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetRotation(gp_Ax1(axis.Location(), axis.YDirection()), angle)
        return transformation

    @staticmethod
    def rotation_y_deg(angle, axis: gp_Ax3 = gp_Ax3()) -> gp_Trsf:
        """Builds rotation around oY

        Parameters
        ------------
        angle: float
            [deg] Rotation angle
        axis: gp_Ax3, optional
            the geometrical reference, default Oxyz

        Returns
        ---------
        transformation: gp_Trfs
            The resulting transformation
        """
        return CreateRotation.rotation_y(radians(angle), axis)

    @staticmethod
    def rotation_z(angle, axis: gp_Ax3 = gp_Ax3()) -> gp_Trsf:
        """Builds rotation around z-axis

        Parameters
        ------------
        angle: float
            [rad] Rotation angle
        axis: gp_Ax3, optional
            the geometrical reference, default Oxyz

        Returns
        ---------
        transformation: gp_Trfs
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetRotation(axis.Axis(), angle)
        return transformation

    @staticmethod
    def rotation_z_deg(angle, axis: gp_Ax3 = gp_Ax3()) -> gp_Trsf:
        """Builds rotation around z-axis

        Parameters
        ------------
        angle: float
            [deg] Rotation angle
        axis: gp_Ax3, optional
            the geometrical reference, default Oxyz

        Returns
        ---------
        transformation: gp_Trfs
            The resulting transformation
        """
        return CreateRotation.rotation_z(radians(angle), axis)

    @staticmethod
    def rotation_z_2d(angle) -> gp_Trsf2d:
        """Builds rotation around oZ

        Parameters
        ------------
        angle: float
            [rad] Rotation angle

        Returns
        ---------
        transformation: gp_Trfs2d
            The resulting transformation
        """
        transformation = gp_Trsf2d()
        transformation.SetRotation(gp_Pnt2d(), angle)
        return transformation

    @staticmethod
    def rotation_z_2d_deg(angle) -> gp_Trsf2d:
        """Builds rotation around oZ

        Parameters
        ------------
        angle: float
            [deg] Rotation angle

        Returns
        ---------
        transformation: gp_Trfs2d
            The resulting transformation
        """
        return CreateRotation.rotation_z_2d(radians(angle))


class CreateScaling:
    """Factory to create scalings."""

    @staticmethod
    def from_factor_and_center(scale_factor: float, center: PointT) -> Union[gp_Trsf, gp_Trsf2d]:
        """Build scale around a center of transformation.

        Parameters
        ------------
        scale_factor: float
            The scaling factor
        center: PointT
            Center of scaling

        Returns
        ---------
        transformation: Union[gp_Trsf, gp_Trsf2d]
            The resulting transformation
        """
        from pyoccad.measure import MeasurePoint

        dim = MeasurePoint.dimension(center)
        if dim == 3:
            transformation = gp_Trsf()
        else:  # dim == 2
            transformation = gp_Trsf2d()

        transformation.SetScale(CreatePoint.as_point(center), scale_factor)
        return transformation

    @staticmethod
    def from_factor(scale_factor: float) -> gp_Trsf:
        """Build a 3D scale factor transformation.

        Parameters
        ------------
        scale_factor: float
            The scaling factor

        Returns
        ---------
        transformation: gp_Trsf
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetScaleFactor(scale_factor)
        return transformation

    @staticmethod
    def from_2d_scale_factor(scale_factor: float) -> gp_Trsf2d:
        """Build a 2D scale factor transformation.

        Parameters
        ------------
        scale_factor: float
            The scaling factor

        Returns
        ---------
        transformation: gp_Trsf2d
            The resulting transformation
        """
        transformation = gp_Trsf2d()
        transformation.SetScaleFactor(scale_factor)
        return transformation


class CreateSymmetry:
    """Factory to create symmetries."""

    @staticmethod
    def from_ox_axis() -> gp_Trsf:
        """Create a symmetry around x-axis.

        Returns
        -------
        transformation: gp_Trsf
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetMirror(CreateAxis.ox())
        return transformation

    @staticmethod
    def from_oy_axis() -> gp_Trsf:
        """Create a symmetry around y-axis.

        Returns
        -------
        transformation: gp_Trsf
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetMirror(CreateAxis.oy())
        return transformation

    @staticmethod
    def from_oz_axis() -> gp_Trsf:
        """Create a symmetry around z-axis.

        Returns
        -------
        transformation: gp_Trsf
            The resulting transformation
        """
        transformation = gp_Trsf()
        transformation.SetMirror(CreateAxis.oz())
        return transformation
