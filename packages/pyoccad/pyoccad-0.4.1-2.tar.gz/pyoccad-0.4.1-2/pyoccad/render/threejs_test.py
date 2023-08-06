from math import pi
from unittest.mock import MagicMock, call

from traitlets import TraitType, TraitError, HasTraits
from pythreejs import (Group, GridHelper, PerspectiveCamera, Scene, AmbientLight, DirectionalLight,
                       LineBasicMaterial, MeshLambertMaterial)

from OCC.Core.Geom import Geom_Curve, Geom_Surface
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh

from pyoccad.create import (CreateCircle, CreateLine, CreateCoordSystem, CreateArc, CreateBezierSurface, CreateWire,
                            CreateFace)
from pyoccad.render.threejs import PyoccadGroup, PyoccadGridHelper, JupyterThreeJSRenderer, ShapeGroup, ShapeInstance
from pyoccad.render.threejs_2d import JupyterThreeJSRenderer2d
from pyoccad.explore import ExploreSubshapes
from pyoccad.tests import TestCase
from pyoccad.transform import Sweep


class PyoccadGroupTest(TestCase):

    def setUp(self):
        self.group = PyoccadGroup()

    def test_init(self):
        self.assertIsInstance(self.group, Group)
        self.assertTrue(hasattr(self.group, "hide"))
        self.assertTrue(hasattr(self.group, "visible"))

    def test_show(self):
        self.group.show()
        self.assertTrue(self.group.visible)

    def test_hide(self):
        self.group.hide()
        self.assertFalse(self.group.visible)


class PyoccadGridHelperTest(TestCase):

    def setUp(self):
        self.helper = PyoccadGridHelper()

    def test_init(self):
        self.assertIsInstance(self.helper, GridHelper)
        self.assertTrue(hasattr(self.helper, "rotateX_deg"))
        self.assertTrue(hasattr(self.helper, "rotateY_deg"))
        self.assertTrue(hasattr(self.helper, "rotateZ_deg"))

        self.assertEqual(self.helper.size, 10.)
        self.assertEqual(self.helper.divisions, 10)
        self.assertEqual(self.helper.colorCenterLine, "#444444")
        self.assertEqual(self.helper.colorGrid, "#888888")
        self.assertTrue(self.helper.visible)

        helper2 = PyoccadGridHelper(colorCenterLine="#333333", colorGrid="#666666")
        self.assertEqual(helper2.colorCenterLine, "#333333")
        self.assertEqual(helper2.colorGrid, "#666666")

    def test_rotateX(self):
        self.helper._send = m = MagicMock()

        self.helper.rotateX()
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateX', 'args': [pi / 2]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

    def test_rotateX_deg(self):
        self.helper._send = m = MagicMock()

        self.helper.rotateX_deg()
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateX', 'args': [pi / 2]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

        m.reset_mock()
        self.helper.rotateX_deg(180)
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateX', 'args': [pi]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

    def test_rotateY(self):
        self.helper._send = m = MagicMock()

        self.helper.rotateY()
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateY', 'args': [pi / 2]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

    def test_rotateY_deg(self):
        self.helper._send = m = MagicMock()

        self.helper.rotateY_deg()
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateY', 'args': [pi / 2]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

        m.reset_mock()
        self.helper.rotateY_deg(180)
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateY', 'args': [pi]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

    def test_rotateZ(self):
        self.helper._send = m = MagicMock()

        self.helper.rotateZ()
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateZ', 'args': [pi / 2]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

    def test_rotateZ_deg(self):
        self.helper._send = m = MagicMock()

        self.helper.rotateZ_deg()
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateZ', 'args': [pi / 2]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

        m.reset_mock()
        self.helper.rotateZ_deg(180)
        m.assert_called_once()

        expected = call({'method': 'custom',
                         'content': {'type': 'exec_three_obj_method', 'method_name': 'rotateZ', 'args': [pi]}},
                        buffers=None)
        self.assertEqual(expected, m.mock_calls[0])

    def test_show(self):
        self.helper.show()
        self.assertTrue(self.helper.visible)

    def test_hide(self):
        self.helper.hide()
        self.assertFalse(self.helper.visible)


class ShapeInstanceTest(TestCase):

    def test___init__(self):

        self.assertIsInstance(ShapeInstance(), TraitType)

        class TestClass(HasTraits):
            shape = ShapeInstance(allow_none=True, default_value=None)

        dummy = TestClass()
        self.assertIsNone(dummy.shape)

        dummy.shape = CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0])
        self.assertIsInstance(dummy.shape, Geom_Curve)

        dummy.shape = CreateBezierSurface.from_poles([[(8., 0., 0.5), (5., 1., 1.), (2., 1.2, 4.)],
                                                            [(10., 0., 0.5), (10., 1., 1.), (10., 1.2, 4.)]])
        self.assertIsInstance(dummy.shape, Geom_Surface)

        dummy.shape = CreateWire.from_element(CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0]))
        self.assertIsInstance(dummy.shape, TopoDS_Shape)

        with self.assertRaises(TraitError):
            dummy.shape = 10.


class ShapeGroupTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.group = ShapeGroup(uid='test')
        cls.bezier_surface = CreateBezierSurface.from_poles([[(8., 0., 0.5), (5., 1., 1.), (2., 1.2, 4.)],
                                                             [(10., 0., 0.5), (10., 1., 1.), (10., 1.2, 4.)]])

        segment1 = CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0])
        coord_system = CreateCoordSystem.as_coord_system(([1, 1, 0], [0, -1, 0], [0, 0, 1]))
        arc = CreateArc.from_angles(coord_system, 0.5, 0, pi / 2)
        segment2 = CreateLine.between_2_points([1.5, 1, 0], [1.5, 2, 0])
        path = [segment1, arc, segment2]
        profile = CreateCircle.from_radius_and_center(0.1, [0, 0])
        sweep1 = Sweep.profile_along_path(profile, path)
        cls.segment = segment1
        cls.pipe = sweep1

    def test___init__(self):
        self.assertIsInstance(self.group, PyoccadGroup)

        self.assertIsInstance(self.group.faces_group, PyoccadGroup)
        self.assertIsInstance(self.group.lattice_group, PyoccadGroup)
        self.assertIsInstance(self.group.edges_group, PyoccadGroup)

        self.assertTrue(self.group.faces_group.name.startswith("@faces@"))
        self.assertTrue(self.group.lattice_group.name.startswith("@lattices@"))
        self.assertTrue(self.group.edges_group.name.startswith("@edges@"))

        self.assertTrue(self.group.plot_edges)
        self.assertFalse(self.group.wireframe)

        self.assertEqual((0, 0), self.group.lattice)
        self.assertEqual("aliceblue", self.group.face_color)
        self.assertEqual("#000000", self.group.line_color)
        self.assertEqual("#222222", self.group.lattice_color)
        self.assertEqual(1., self.group.line_width)
        self.assertEqual(1., self.group.opacity)

        self.assertEqual(0.01, self.group.linear_deflection)
        self.assertEqual(0.05, self.group.angular_deflection)
        self.assertEqual(0.01, self.group.curvature_deflection)
        self.assertEqual(2, self.group.min_discretization)

        self.assertIsInstance(self.group.face_material, MeshLambertMaterial)
        self.assertIsInstance(self.group.line_material, LineBasicMaterial)
        self.assertIsInstance(self.group.lattice_material, LineBasicMaterial)

        self.assertEqual('test', self.group.name)
        self.assertIsNone(self.group.shape)
        self.assertEqual(True, self.group.visible)

        self.assertIsInstance(self.group._mapping, dict)
        self.assertEqual(0, len(self.group._mapping))

        g = ShapeGroup(CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0]))
        self.assertEqual(3, len(g))
        for name in ("@faces@", "@lattices@", "@edges@"):
            self.assertEqual(1, len([leaf for leaf in g.children if leaf.name.startswith(name)]))

    def test__default_face_material(self):
        self.assertEqual(self.group.wireframe, self.group.face_material.wireframe)
        self.assertEqual(self.group.face_color, self.group.face_material.color)
        self.assertEqual(self.group.opacity, self.group.face_material.opacity)
        self.assertEqual(self.group.opacity < 1., self.group.face_material.transparent)

    def test__default_line_material(self):
        self.assertEqual(self.group.line_width, self.group.line_material.linewidth)
        self.assertEqual(self.group.line_color, self.group.line_material.color)

    def test__default_lattice_material(self):
        self.assertEqual(self.group.line_width, self.group.lattice_material.linewidth)
        self.assertEqual(self.group.lattice_color, self.group.lattice_material.color)

    def test__validate_shape(self):
        self.group.shape = CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0])
        self.assertIsInstance(self.group.shape, TopoDS_Shape)

        bezier_surface = CreateBezierSurface.from_poles([[(8., 0., 0.5), (5., 1., 1.), (2., 1.2, 4.)],
                                                         [(10., 0., 0.5), (10., 1., 1.), (10., 1.2, 4.)]])
        self.group.shape = bezier_surface
        self.assertIsInstance(self.group.shape, TopoDS_Shape)

        wire = CreateWire.from_element(CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0]))
        self.group.shape = wire
        self.assertIsInstance(self.group.shape, TopoDS_Shape)

    def test__observe_line_color(self):
        for color in ('yellow', 'red', 'blue', 'aliceblue'):
            self.group.line_color = color
            self.assertEqual(color, self.group.line_material.color)

    def test__observe_lattice_color(self):
        for color in ('yellow', 'red', 'blue', 'aliceblue'):
            self.group.lattice_color = color
            self.assertEqual(color, self.group.lattice_material.color)

    def test__observe_face_color(self):
        for color in ('yellow', 'red', 'blue', 'aliceblue'):
            self.group.face_color = color
            self.assertEqual(color, self.group.face_material.color)

    def test__observe_wireframe(self):
        self.group.wireframe = True
        self.assertTrue(self.group.face_material.wireframe)

        self.group.wireframe = False
        self.assertFalse(self.group.face_material.wireframe)

    def test__get_face_mesh(self):
        shape = CreateFace.from_contour(self.bezier_surface)
        shape_faces = [f for f in ExploreSubshapes.get_faces(shape)]

        with self.assertRaises(RuntimeError):
            ShapeGroup._get_face_mesh(shape_faces[0])

        BRepMesh_IncrementalMesh(shape, 0.01, True, 0.05, True)
        vertices, faces, pos, quat = ShapeGroup._get_face_mesh(shape_faces[0])
        self.assertTrue(len(vertices) > 0)
        self.assertTrue(len(faces) > 0)
        self.assertTrue(len(pos) > 0)
        self.assertTrue(len(quat) > 0)

    def test__build_shape_faces(self):
        self.assertEqual(0, len(self.group.faces_group.children))

        self.group.shape = self.pipe
        self.assertEqual(1, len(self.group.faces_group.children))

        self.group.shape = self.bezier_surface
        self.assertEqual(1, len(self.group.faces_group.children))

    def test__build_shape_lattice(self):
        self.group.shape = self.bezier_surface
        self.assertEqual(0, len(self.group.lattice_group.children))

        for lattice in [(4, 3), (2, 2), (0, 0)]:
            self.group.lattice = lattice
            expected = 1 if lattice != (0, 0) else 0
            self.assertEqual(expected, len(self.group.lattice_group.children))

    def test__build_shape_edges(self):
        self.group.shape = self.bezier_surface
        self.assertEqual(1, len(self.group.edges_group.children))

        self.group.shape = self.pipe
        self.assertEqual(1, len(self.group.edges_group.children))

        self.group.shape = self.segment
        self.assertEqual(1, len(self.group.edges_group.children))

        self.group.plot_edges = False
        self.assertEqual(1, len(self.group.edges_group.children))
        self.assertFalse(self.group.edges_group.visible)  # just hide the group

        self.group.plot_edges = True  # set option to default to not pollute other tests
        self.assertTrue(self.group.edges_group.visible)

    def test__update_curve(self):
        self.group.shape = self.bezier_surface
        edge = self.group.edges_group.children[0]

        wire = CreateWire.from_element(self.segment)
        with self.assertRaises(ValueError):
            self.group._update_curve(wire, uid='test')

        self.group._update_curve(wire, uid=edge.name)


class JupyterThreeJSRendererTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.ren = JupyterThreeJSRenderer()
   
        segment1 = CreateLine.between_2_points([0, 0.5, 0], [1, 0.5, 0])
        coord_system = CreateCoordSystem.as_coord_system(([1, 1, 0], [0, -1, 0], [0, 0, 1]))
        arc = CreateArc.from_angles(coord_system, 0.5, 0, pi / 2)
        segment2 = CreateLine.between_2_points([1.5, 1, 0], [1.5, 2, 0])
        path = [segment1, arc, segment2]
        profile = CreateCircle.from_radius_and_center(0.1, [0, 0])
        sweep1 = Sweep.profile_along_path(profile, path)

        cls.ren.add_shape(sweep1, 'pipe', lattice=(0, 0), opacity=1., plot_edges=True)
        cls.pipe = sweep1
        cls.bezier_surface = CreateBezierSurface.from_poles([[(8., 0., 0.5), (5., 1., 1.), (2., 1.2, 4.)],
                                                             [(10., 0., 0.5), (10., 1., 1.), (10., 1.2, 4.)]])

    def test_init(self):
        self.assertIsInstance(self.ren._scene, Scene)
        self.assertIsInstance(self.ren._cam, PerspectiveCamera)
        self.assertIsInstance(self.ren._ax, PyoccadGroup)
        self.assertIsInstance(self.ren._grid, GridHelper)
        self.assertIsInstance(self.ren._displayed, PyoccadGroup)

    def test_add_axes(self):
        self.ren.add_axes(10.)
        axes = [group for group in self.ren._scene.children if group.name.startswith("@axes@")]
        self.assertIsInstance(axes[-1], PyoccadGroup)
        self.assertIs(axes[-1], self.ren._ax)

    def test_add_camera(self):
        self.ren.add_camera((60, 60, 80), fov=10.)
        self.assertIsInstance(self.ren._scene.children[-1], PerspectiveCamera)
        self.assertIs(self.ren._scene.children[-1], self.ren._cam)

    def test_add_ambient_light(self):
        self.ren.add_ambient_light()
        self.assertIsInstance(self.ren._scene.children[-1], AmbientLight)

    def test_add_directional_light(self):
        self.ren.add_directional_light((10, 100, 1000))
        self.assertIsInstance(self.ren._scene.children[-1], DirectionalLight)

    def test_add_grid(self):
        self.assertTrue(self.ren._grid in self.ren._scene.children)

        g = self.ren._grid
        self.assertEqual(20, g.size)
        self.assertEqual(20, g.divisions)
        self.assertEqual("#444444", g.colorCenterLine)
        self.assertEqual("#444444", g.colorGrid)

    def test__mapping(self):
        self.assertEqual(1, len(self.ren._mapping))
        shape_group = self.ren._displayed.children[0]
        self.assertEqual(shape_group, self.ren._mapping['pipe'])
        self.assertIsInstance(shape_group, ShapeGroup)

    def test_add_shape(self):
        self.ren.clear_shapes()
        self.ren.add_shape(self.pipe, 'pipe')

        displayed_shapes = [group.name for group in self.ren._displayed.children]
        self.assertEqual(1, len(displayed_shapes))
        self.assertEqual("pipe", displayed_shapes[0])

        self.ren.add_shape(self.bezier_surface)
        self.assertEqual(2, len([(group.name, group) for group in self.ren._displayed.children]))

        with self.assertRaises(AttributeError):
            self.ren.add_shape(self.bezier_surface, uid="pipe")

        self.ren.add_shape(self.bezier_surface, uid="pipe", force=True)
        self.assertEqual(2, len([(group.name, group) for group in self.ren._displayed.children]))

    def test_update_shape(self):
        self.ren.clear_shapes()
        group = self.ren.add_shape(self.pipe, 'pipe')

        displayed_shapes = [group.name for group in self.ren._displayed.children]
        self.assertEqual(1, len(displayed_shapes))
        self.assertEqual("pipe", displayed_shapes[0])
        self.assertEqual(1, len(group.faces_group.children))
        self.assertEqual(1, len(group.edges_group.children))

        group = self.ren.update_shape(self.bezier_surface, uid="pipe")
        self.assertEqual(1, len([group.name for group in self.ren._displayed.children]))
        self.assertEqual(1, len(group.faces_group.children))
        self.assertEqual(1, len(group.edges_group.children))

        with self.assertRaises(KeyError):
            self.ren.update_shape(self.bezier_surface, uid='dummy')

    def test_get_shape(self):
        self.ren.clear_shapes()
        self.ren.add_shape(self.pipe, 'pipe')

        group = self.ren.get_shape('pipe')
        self.assertEqual('pipe', group.name)
        self.assertEqual(1, len(group.faces_group.children))
        self.assertEqual(1, len(group.edges_group.children))

        with self.assertRaises(KeyError):
            self.ren.get_shape(uid='dummy')

    def test_remove_shape(self):
        self.ren.clear_shapes()
        self.ren.add_shape(self.pipe, 'pipe')
        self.ren.remove_shape('pipe')
        self.assertEqual(0, len(self.ren._displayed.children))

        with self.assertRaises(KeyError):
            self.ren.remove_shape(uid='dummy')

    def test__validate_camera_aspect_ratio(self):
        self.ren.shape = self.pipe
        self.ren.camera_aspect_ratio = -0.1
        self.assertEqual(0.1, self.ren.camera_aspect_ratio)

    def test__observe_view_size(self):
        height = 455
        width = 654

        self.ren.view_size = (width, height)
        self.assertEqual(width / height, self.ren.camera_aspect_ratio)

    def test__observe_camera_aspect_ratio(self):
        aspect_ratio = 1.65
        self.ren.view_size = (800, 600)

        self.ren.camera_aspect_ratio = aspect_ratio
        self.assertEqual(self.ren.view_size[0], int(600*aspect_ratio))
        self.assertEqual(aspect_ratio, self.ren._cam.aspect)

    def test__observe_camera_position(self):
        for camera_position in ((10., 20., 30.), (0., 0., 0.), (1., 1., 1.)):
            self.ren.camera_position = camera_position
            self.assertEqual(camera_position, self.ren._cam.position)

    def test__update_view(self):
        for width, height in [(800, 600), (455, 698), (788, 455)]:
            self.ren.view_size = (width, height)
            self.assertEqual(width, self.ren._renderer.width)
            self.assertEqual(height, self.ren._renderer.height)

    def test__observe_background_color(self):
        for color in ['red', 'blue', 'yellow']:
            self.ren.background_color = color
            self.assertEqual(color, self.ren._scene.background)


class JupyterThreeJSRenderer2dTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.ren = JupyterThreeJSRenderer2d()

    def test_init(self):
        self.assertEqual((0., 0., 3.), self.ren._cam.position)
