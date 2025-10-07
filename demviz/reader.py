import cv2
import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

class DEMReader:
    """Handles loading and processing of DEM data using GDAL."""
    def __init__(self, dem_path):
        self.dem_path = dem_path
        self.dataset = None
        self.elevation = None
        self.min_elev = None
        self.max_elev = None
        self.transform = None
        self.crs = None
        self.rows = None
        self.cols = None

    def load(self):
        """Load DEM file and extract metadata including CRS."""
        try:
            self.dataset = gdal.Open(self.dem_path)
            if not self.dataset:
                raise FileNotFoundError(f"Could not open DEM: {self.dem_path}")
            
            band = self.dataset.GetRasterBand(1)
            stats = band.GetStatistics(True, True)
            self.min_elev, self.max_elev = stats[0], stats[1]
            self.elevation = band.ReadAsArray().astype(np.float32)
            self.rows, self.cols = self.elevation.shape
            self.transform = self.dataset.GetGeoTransform()
            self.crs = osr.SpatialReference()
            self.crs.ImportFromWkt(self.dataset.GetProjection())

            nodata = band.GetNoDataValue()
            if nodata is not None:
                self.elevation[self.elevation == nodata] = np.nan
            self.elevation = np.nan_to_num(self.elevation, nan=self.min_elev)
        except Exception as e:
            raise RuntimeError(f"Error loading DEM: {e}")

    def normalize_elevation(self, smooth=True):
        """Normalize elevation data to 0–255 and optionally smooth it."""
        elevation_norm = ((self.elevation - self.min_elev) / (self.max_elev - self.min_elev)) * 255.0
        elevation_norm = np.clip(elevation_norm, 0, 255).astype(np.float32)
        if smooth:
            elevation_norm = cv2.GaussianBlur(elevation_norm, (5, 5), 0)
        return elevation_norm

    def get_projected_bounds(self):
        """Calculate the projected bounds of the DEM."""
        x_min, x_res, _, y_max, _, y_res = self.transform
        x_max = x_min + self.cols * x_res
        y_min = y_max + self.rows * y_res
        return x_min, x_max, y_min, y_max

    def pixel_to_projected(self, x, y):
        """Convert pixel coordinates to projected coordinates."""
        x_proj = self.transform[0] + x * self.transform[1] + y * self.transform[2]
        y_proj = self.transform[3] + x * self.transform[4] + y * self.transform[5]
        return x_proj, y_proj