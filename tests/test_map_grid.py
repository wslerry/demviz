import unittest
import numpy as np
import vtk
from osgeo import osr
from demviz.map_grid import VTKMapGridOverlay

class TestVTKMapGridOverlay(unittest.TestCase):
    def setUp(self):
        # Mock CRS and bounds
        self.x_min, self.x_max = 0, 1000
        self.y_min, self.y_max = 0, 1000
        self.crs = osr.SpatialReference()
        self.crs.ImportFromEPSG(32633)  # UTM Zone 33N
        self.rows, self.cols = 10, 10
        self.z_height = 0

    def test_create_grid_actor(self):
        grid_overlay = VTKMapGridOverlay(self.x_min, self.x_max, self.y_min, self.y_max, self.crs, self.rows, self.cols)
        grid_actor = grid_overlay.create_grid_actor(grid_spacing=200, num_lines=5)
        
        # Check actor properties
        self.assertIsInstance(grid_actor, vtk.vtkActor)
        self.assertIsInstance(grid_actor.GetMapper().GetInput(), vtk.vtkPolyData)
        
        # Check grid lines
        poly_data = grid_actor.GetMapper().GetInput()
        self.assertGreater(poly_data.GetNumberOfLines(), 0)
        self.assertEqual(grid_actor.GetProperty().GetColor(), (1.0, 0.0, 0.0))  # Red lines

    def test_grid_spacing_geographic(self):
        # Test with geographic CRS (lat/lon)
        self.crs = osr.SpatialReference()
        self.crs.ImportFromEPSG(4326)  # WGS84
        grid_overlay = VTKMapGridOverlay(self.x_min, self.x_max, self.y_min, self.y_max, self.crs, self.rows, self.cols)
        grid_actor = grid_overlay.create_grid_actor(grid_spacing=0.005)  # Below minimum
        poly_data = grid_actor.GetMapper().GetInput()
        self.assertGreater(poly_data.GetNumberOfLines(), 0)

if __name__ == "__main__":
    unittest.main()