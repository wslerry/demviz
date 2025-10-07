import vtk

class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    """Custom interactor style for controlling the VTK scene."""
    def __init__(self, renderer, actor, parent=None):
        super().__init__(parent)
        self.renderer = renderer
        self.actor = actor
        self.AddObserver("KeyPressEvent", self.onKeyPress)

    def onKeyPress(self, obj, event):
        """Handle key press events for interaction."""
        key = self.GetInteractor().GetKeySym()
        cam = self.renderer.GetActiveCamera()
        if key == "r":
            print("Resetting camera")
            self.renderer.ResetCamera()
        elif key == "w":
            print("View mode: Wireframe")
            self.actor.GetProperty().SetRepresentationToWireframe()
        elif key == "s":
            print("View mode: Surface")
            self.actor.GetProperty().SetRepresentationToSurface()
        elif key == "p":
            print("View mode: Points")
            self.actor.GetProperty().SetRepresentationToPoints()
        elif key == "plus":
            cam.Zoom(1.2)
        elif key == "minus":
            cam.Zoom(0.8)
        elif key == "Up":
            cam.Elevation(5)
        elif key == "Down":
            cam.Elevation(-5)
        elif key == "Left":
            cam.Azimuth(-5)
        elif key == "Right":
            cam.Azimuth(5)
        self.GetInteractor().GetRenderWindow().Render()