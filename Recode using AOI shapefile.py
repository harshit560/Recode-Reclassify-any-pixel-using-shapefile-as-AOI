#!/usr/bin/env python

#Recode using AOI to and change the pixel value
import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping
def update_and_merge_pixels(input_raster, shapefile_path, output_raster, new_value):
    # Open input raster file
    with rasterio.open(input_raster) as src:
        # Read the raster data
        raster_data = src.read(1)
        # Get the transform
        transform = src.transform
        
        # Open shapefile
        gdf = gpd.read_file(shapefile_path)
        
        # Check CRS
        if gdf.crs != src.crs:
            raise ValueError("CRS mismatch between shapefile and raster.")
        
        # Get the geometry from the shapefile
        shapefile_geometry = gdf.geometry.iloc[0]
        
        # Convert shapefile geometry to pixel coordinates
        # This step assumes that the shapefile and raster are aligned and have the same resolution
        mask = rasterio.features.geometry_mask([shapefile_geometry], out_shape=raster_data.shape, transform=transform, invert=True)
        
        # Update pixel values within the masked area
        raster_data[mask] = new_value
        
        # Write the updated raster to output file
        with rasterio.open(output_raster, "w", **src.profile) as dest:
            dest.write(raster_data, 1)

# Example usage: use your path
input_raster = "C:\\Users\\Hp\\Desktop\\Ladakh\\Sample_raster.tif"
shapefile_path = "C:\\Users\\Hp\\Desktop\\Ladakh\\sample_AOI.shp"
output_raster = "C:\\Users\\Hp\\Desktop\\Ladakh\\output_image.tif"
new_value = 3  # New pixel value

update_and_merge_pixels(input_raster, shapefile_path, output_raster, new_value)






