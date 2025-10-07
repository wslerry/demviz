import unittest
from unittest.mock import Mock
import vtk
from demviz.interactor import CustomInteractorStyle

class TestCustomInteractorStyle(unittest.TestCase):
    def setUp(self):
        # Mock VTK objects
        self.renderer = Mock(spec=vtk.vtkRenderer)
        self.actor = Mock(spec=vtk.vtkActor)
        self.actor.GetProperty.return_value = Mock()
        self.renderer.GetActiveCamera.return_value = Mock()
        self.interactor = Mock()
        self.interactor.GetRenderWindow.return_value = Mock()
        self.interactor.GetKeySym = Mock()  # Explicitly mock GetKeySym
        self.style = CustomInteractorStyle(self.renderer, self.actor)

    def test_keypress_reset(self):
        self.interactor.GetKeySym.return_value = "r"
        self.style.onKeyPress(None, None)
        self.renderer.ResetCamera.assert_called_once()

    def test_keypress_wireframe(self):
        self.interactor.GetKeySym.return_value = "w"
        self.style.onKeyPress(None, None)
        self.actor.GetProperty().SetRepresentationToWireframe.assert_called_once()

    def test_keypress_surface(self):
        self.interactor.GetKeySym.return_value = "s"
        self.style.onKeyPress(None, None)
        self.actor.GetProperty().SetRepresentationToSurface.assert_called_once()

    def test_keypress_points(self):
        self.interactor.GetKeySym.return_value = "p"
        self.style.onKeyPress(None, None)
        self.actor.GetProperty().SetRepresentationToPoints.assert_called_once()

    def test_keypress_zoom_in(self):
        self.interactor.GetKeySym.return_value = "plus"
        self.style.onKeyPress(None, None)
        self.renderer.GetActiveCamera().Zoom.assert_called_once_with(1.2)

    def test_keypress_zoom_out(self):
        self.interactor.GetKeySym.return_value = "minus"
        self.style.onKeyPress(None, None)
        self.renderer.GetActiveCamera().Zoom.assert_called_once_with(0.8)

    def test_keypress_rotate_up(self):
        self.interactor.GetKeySym.return_value = "Up"
        self.style.onKeyPress(None, None)
        self.renderer.GetActiveCamera().Elevation.assert_called_once_with(5)

    def test_keypress_rotate_down(self):
        self.interactor.GetKeySym.return_value = "Down"
        self.style.onKeyPress(None, None)
        self.renderer.GetActiveCamera().Elevation.assert_called_once_with(-5)

    def test_keypress_rotate_left(self):
        self.interactor.GetKeySym.return_value = "Left"
        self.style.onKeyPress(None, None)
        self.renderer.GetActiveCamera().Azimuth.assert_called_once_with(-5)

    def test_keypress_rotate_right(self):
        self.interactor.GetKeySym.return_value = "Right"
        self.style.onKeyPress(None, None)
        self.renderer.GetActiveCamera().Azimuth.assert_called_once_with(5)

if __name__ == "__main__":
    unittest.main()