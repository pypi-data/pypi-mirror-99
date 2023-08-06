from pythreejs import PerspectiveCamera, DirectionalLight
from traitlets import Tuple, Float

from pyoccad.render.threejs import JupyterThreeJSRenderer
from pyoccad.typing import Point3T


class JupyterThreeJSRenderer2d(JupyterThreeJSRenderer):
    """2D renderer using pyThreeJS"""

    camera_position = Tuple(Float(), Float(), Float(), default_value=(0., 0., 3.))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cc.enableRotate = False

    def add_camera(self, position: Point3T, fov: float = 75, near: float = 0.1, far: float = 1000, aspect: float = 1):
        """
        Add a camera to the scene.

        Parameters
        ----------
        position : Point3T
            the camera position
        fov : float, optional
            the camera field of view
        near : float, optional
            the minimum distance visible to the camera
        far : float, optional
            the maximum distance visible to the camera
        aspect : float, optional
            the camera aspect ratio
        """
        # TODO: understand why the OrthographicCamera does not work
        cam = PerspectiveCamera(
            position=position, fov=fov, aspect=aspect, near=near, far=far,
            children=[DirectionalLight(color='#ffffff', position=position, intensity=0.9)]
        )
        self._cam = cam
        self._scene.add(cam)
