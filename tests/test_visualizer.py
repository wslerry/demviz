import unittest
import os
from unittest.mock import patch
from demviz.visualizer import DEMVisualizer
from demviz.reader import DEMReader

class TestDEMVisualizer(unittest.TestCase):
    def setUp(self):
        self.dem_path = "tests/sains_dsm.tif"  # Updated path
        if not os.path.exists(self.dem_path):
            self.skipTest("Test DEM file not found")

    @patch("demviz.visualizer.vtk.vtkRenderer")
    @patch("demviz.visualizer.vtk.vtkRenderWindow")
    @patch("demviz.visualizer.vtk.vtkRenderWindowInteractor")
    def test_setup_scene(self, mock_interactor, mock_window, mock_renderer):
        visualizer = DEMVisualizer(self.dem_path, z_scale=0.05, smooth=True, grid_spacing=1000)
        visualizer.setup_scene()
        
        # Check that renderer, window, and interactor are set up
        self.assertIsNotNone(visualizer.renderer)
        self.assertIsNotNone(visualizer.window)
        self.assertIsNotNone(visualizer.interactor)
        self.assertIsNotNone(visualizer.actor)
        
        # Verify actors were added to renderer
        self.assertGreater(visualizer.renderer.GetActors().GetNumberOfItems(), 0)
        self.assertGreater(visualizer.renderer.GetViewProps().GetNumberOfItems(), 0)

    def test_initialization(self):
        visualizer = DEMVisualizer(self.dem_path, z_scale=0.05, smooth=True, grid_spacing=1000)
        self.assertEqual(visualizer.dem_path, self.dem_path)
        self.assertEqual(visualizer.z_scale, 0.05)
        self.assertTrue(visualizer.smooth)
        self.assertEqual(visualizer.grid_spacing, 1000)

if __name__ == "__main__":
    unittest.main()