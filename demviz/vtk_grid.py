import vtk
import numpy as np
from vtk.util import numpy_support

class VTKGridCreator:
    """Creates VTK structured grid from elevation data."""
    def __init__(self, elevation_norm, rows, cols, transform, z_scale=1.5):
        self.elevation_norm = elevation_norm
        self.rows = rows
        self.cols = cols
        self.transform = transform
        self.z_scale = z_scale

    def create_grid(self):
        """Create a VTK structured grid with projected coordinates."""
        points = vtk.vtkPoints()
        for y in range(self.rows):
            for x in range(self.cols):
                x_proj, y_proj = self.pixel_to_projected(x, y)
                z = float(self.elevation_norm[y, x]) * self.z_scale
                points.InsertNextPoint(x_proj, y_proj, z)

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(self.cols, self.rows, 1)
        grid.SetPoints(points)

        vtk_elev = numpy_support.numpy_to_vtk(self.elevation_norm.flatten(), deep=True, array_type=vtk.VTK_FLOAT)
        grid.GetPointData().SetScalars(vtk_elev)
        return grid

    def pixel_to_projected(self, x, y):
        """Convert pixel coordinates to projected coordinates."""
        x_proj = self.transform[0] + x * self.transform[1] + y * self.transform[2]
        y_proj = self.transform[3] + x * self.transform[4] + y * self.transform[5]
        return x_proj, y_proj