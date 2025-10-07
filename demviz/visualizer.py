import vtk
from .reader import DEMReader
from .vtk_grid import VTKGridCreator
from .map_grid import VTKMapGridOverlay
from .interactor import CustomInteractorStyle

class DEMVisualizer:
    """Main class for visualizing DEM data with VTK."""
    def __init__(self, dem_path, z_scale=1.5, smooth=True, grid_spacing=None):
        self.dem_path = dem_path
        self.z_scale = z_scale
        self.smooth = smooth
        self.grid_spacing = grid_spacing
        self.renderer = vtk.vtkRenderer()
        self.window = vtk.vtkRenderWindow()
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.actor = None

    def setup_scene(self):
        """Set up the VTK scene with DEM data and map grid overlay."""
        # Load and process DEM
        dem_reader = DEMReader(self.dem_path)
        dem_reader.load()
        elevation_norm = dem_reader.normalize_elevation(smooth=self.smooth)
        x_min, x_max, y_min, y_max = dem_reader.get_projected_bounds()

        # Create VTK grid in projected coordinates
        grid_creator = VTKGridCreator(elevation_norm, dem_reader.rows, dem_reader.cols, dem_reader.transform, self.z_scale)
        grid = grid_creator.create_grid()

        # Set up mapper and actor
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(grid)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(0.9, 0.9, 0.9)
        self.actor.GetProperty().SetAmbient(0.3)
        self.actor.GetProperty().SetDiffuse(0.7)
        self.actor.GetProperty().SetSpecular(0.2)

        # Add actor to renderer
        self.renderer.AddActor(self.actor)

        # Add map grid overlay
        grid_overlay = VTKMapGridOverlay(x_min, x_max, y_min, y_max, dem_reader.crs, dem_reader.rows, dem_reader.cols)
        grid_actor = grid_overlay.create_grid_actor(grid_spacing=self.grid_spacing)
        self.renderer.AddActor(grid_actor)

        # Set up lighting
        light = vtk.vtkLight()
        light.SetLightTypeToSceneLight()
        light.SetPosition(-1, -1, 1)
        light.SetIntensity(1.2)
        self.renderer.AddLight(light)

        # Set background
        self.renderer.SetBackground(0.2, 0.3, 0.4)

        # Add help text
        text = vtk.vtkTextActor()
        text.SetInput("[r] Reset  [w] Wireframe  [s] Surface  [p] Point  [+/-] Zoom  [Arrows] Rotate")
        text.GetTextProperty().SetFontSize(14)
        text.GetTextProperty().SetColor(1, 1, 1)
        text.SetDisplayPosition(10, 10)
        self.renderer.AddViewProp(text)

        # Set up window and interactor
        self.window.AddRenderer(self.renderer)
        self.interactor.SetRenderWindow(self.window)
        style = CustomInteractorStyle(self.renderer, self.actor)
        self.interactor.SetInteractorStyle(style)

        # Add orientation widget
        axes = vtk.vtkAxesActor()
        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)
        widget.SetViewport(0.0, 0.0, 0.15, 0.3)
        widget.SetInteractor(self.interactor)
        widget.EnabledOn()
        widget.InteractiveOn()

    def render(self):
        """Render the scene and start interaction."""
        self.renderer.ResetCamera()
        self.window.Render()
        self.interactor.Start()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Visualize a DEM file with VTK.")
    parser.add_argument("dem_path", help="Path to the DEM file (e.g., GeoTIFF)")
    parser.add_argument("--z-scale", type=float, default=1.5, help="Z-axis scaling factor for elevation")
    parser.add_argument("--no-smooth", action="store_false", dest="smooth", help="Disable Gaussian smoothing")
    parser.add_argument("--grid-spacing", type=float, default=None, help="Grid spacing in projected units")
    args = parser.parse_args()

    try:
        visualizer = DEMVisualizer(args.dem_path, z_scale=args.z_scale, smooth=args.smooth, grid_spacing=args.grid_spacing)
        visualizer.setup_scene()
        visualizer.render()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())