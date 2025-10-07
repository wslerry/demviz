import unittest
import numpy as np
import vtk
from demviz.vtk_grid import VTKGridCreator

class TestVTKGridCreator(unittest.TestCase):
    def setUp(self):
        # Mock elevation data and transform
        self.elevation_norm = np.ones((10, 10), dtype=np.float32) * 100.0  # 10x10 grid
        self.rows, self.cols = self.elevation_norm.shape
        self.transform = (0, 1, 0, 0, 0, -1)  # Simple geotransform
        self.z_scale = 1.5

    def test_create_grid(self):
        grid_creator = VTKGridCreator(self.elevation_norm, self.rows, self.cols, self.transform, self.z_scale)
        grid = grid_creator.create_grid()
        
        # Check grid properties
        self.assertIsInstance(grid, vtk.vtkStructuredGrid)
        dims = [0, 0, 0]
        grid.GetDimensions(dims)  # Pass an array to store dimensions
        self.assertEqual(tuple(dims), (self.cols, self.rows, 1))
        self.assertEqual(grid.GetNumberOfPoints(), self.rows * self.cols)
        
        # Check a sample point
        x, y, z = grid.GetPoint(0)  # First point
        expected_x, expected_y = grid_creator.pixel_to_projected(0, 0)
        expected_z = float(self.elevation_norm[0, 0]) * self.z_scale
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(y, expected_y)
        self.assertAlmostEqual(z, expected_z)

    def test_pixel_to_projected(self):
        grid_creator = VTKGridCreator(self.elevation_norm, self.rows, self.cols, self.transform, self.z_scale)
        x, y = grid_creator.pixel_to_projected(5, 5)
        expected_x = self.transform[0] + 5 * self.transform[1] + 5 * self.transform[2]
        expected_y = self.transform[3] + 5 * self.transform[4] + 5 * self.transform[5]
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(y, expected_y)

if __name__ == "__main__":
    unittest.main()