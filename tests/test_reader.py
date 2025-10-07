import unittest
import os
from demviz.reader import DEMReader

class TestDEMReader(unittest.TestCase):
    def setUp(self):
        self.dem_path = "tests/srtm.tif"  # Updated path to ensure it's in tests/
        if not os.path.exists(self.dem_path):
            self.skipTest("Test DEM file not found")

    def test_load(self):
        reader = DEMReader(self.dem_path)
        reader.load()
        self.assertIsNotNone(reader.dataset)
        self.assertIsNotNone(reader.elevation)
        self.assertIsNotNone(reader.transform)
        self.assertIsNotNone(reader.crs)

    def test_normalize_elevation(self):
        reader = DEMReader(self.dem_path)
        reader.load()
        elevation_norm = reader.normalize_elevation(smooth=False)
        self.assertTrue((elevation_norm >= 0).all())
        self.assertTrue((elevation_norm <= 255).all())

if __name__ == "__main__":
    unittest.main()