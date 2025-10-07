import vtk
import numpy as np

class VTKMapGridOverlay:
    """Creates a map grid overlay based on the DEM's projection."""
    def __init__(self, x_min, x_max, y_min, y_max, crs, rows, cols, z_height=0):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.crs = crs
        self.rows = rows
        self.cols = cols
        self.z_height = z_height

    def create_grid_actor(self, grid_spacing=None, num_lines=10):
        """Create a map grid actor in the DEM's projected coordinate system."""
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()

        # Determine grid spacing based on projection
        if grid_spacing is None:
            x_range = self.x_max - self.x_min
            y_range = self.y_max - self.y_min
            grid_spacing_x = x_range / num_lines
            grid_spacing_y = y_range / num_lines
        else:
            grid_spacing_x = grid_spacing_y = grid_spacing

        # Adjust grid spacing for lat/lon (degrees) vs. projected (meters)
        if self.crs.IsGeographic():
            grid_spacing_x = max(grid_spacing_x, 0.01)  # Minimum 0.01 degrees
            grid_spacing_y = max(grid_spacing_y, 0.01)
        else:
            grid_spacing_x = max(grid_spacing_x, 1.0)  # Minimum 1 meter
            grid_spacing_y = max(grid_spacing_y, 1.0)

        # Calculate grid line positions
        x_steps = np.arange(self.x_min, self.x_max + grid_spacing_x, grid_spacing_x)
        y_steps = np.arange(self.y_min, self.y_max + grid_spacing_y, grid_spacing_y)

        # Horizontal lines (constant y)
        point_id = 0
        for y in y_steps:
            for x in np.linspace(self.x_min, self.x_max, self.cols):
                points.InsertNextPoint(x, y, self.z_height)
                if x < self.x_max:
                    line = vtk.vtkLine()
                    line.GetPointIds().SetId(0, point_id)
                    line.GetPointIds().SetId(1, point_id + 1)
                    lines.InsertNextCell(line)
                point_id += 1

        # Vertical lines (constant x)
        for x in x_steps:
            for y in np.linspace(self.y_min, self.y_max, self.rows):
                points.InsertNextPoint(x, y, self.z_height)
                if y < self.y_max:
                    line = vtk.vtkLine()
                    line.GetPointIds().SetId(0, point_id)
                    line.GetPointIds().SetId(1, point_id + 1)
                    lines.InsertNextCell(line)
                point_id += 1

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetLines(lines)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly_data)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Red grid lines
        actor.GetProperty().SetLineWidth(1.5)
        return actor