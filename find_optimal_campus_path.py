"""
Campus Route Finder
===================
This script calculates the optimal pedestrian route between two points on campus,
prioritizing indoor pathways where available. It uses cost distance analysis with
a pre-defined cost raster that favors indoor routes over outdoor paths.
Author: Jacob Wysko
Date: November 2025
"""
import arcpy
CAMPUS_ROUTE = "CampusRoute"
def find_campus_route(pointOfBeginning, pointOfEnding, costRaster):
    """
    Finds the optimal pedestrian route between two campus locations.
    
    This function performs cost distance analysis using a campus-specific cost raster
    that assigns lower costs to indoor pathways, encouraging routes that stay indoors
    when possible. The analysis consists of two main steps:
    1. Distance accumulation from start point using cost surface
    2. Optimal path calculation from destination back to start
    
    Args:
        pointOfBeginning (str): Path to starting point feature layer
        pointOfEnding (str): Path to destination point feature layer
        costRaster (str): Pre-computed cost raster, prioritizing indoor walkways
        
    Returns:
        None: Output is written to geodatabase feature class
    """
    try:
        # Step 1: Calculate distance accumulation from starting point
        arcpy.AddMessage("Calculating distance accumulation from start point...")
        distanceAccumulationRaster = arcpy.sa.DistanceAccumulation(
            in_source_data=pointOfBeginning,
            in_barrier_data=None,             
            in_surface_raster=None,           
            in_cost_raster=costRaster,
            in_vertical_raster=None,             
            vertical_factor="BINARY 1 -30 30",
            in_horizontal_raster=None,
            horizontal_factor="BINARY 1 45",  
            out_back_direction_raster=r"memory\campus_route_back_direction",
            out_source_direction_raster=None,
            out_source_location_raster=None,
            source_initial_accumulation=None,
            source_maximum_accumulation=None,
            source_cost_multiplier=None,
            source_direction="",
            distance_method="PLANAR"         
        )
        
        # Step 2: Perform optimal path analysis
        arcpy.AddMessage("Calculating optimal path...")
        arcpy.sa.OptimalPathAsLine(
            in_destination_data=pointOfEnding,
            in_distance_accumulation_raster=distanceAccumulationRaster,
            in_back_direction_raster=r"memory\campus_route_back_direction",
            out_polyline_features=CAMPUS_ROUTE,
            destination_field="OBJECTID",        
            path_type="EACH_ZONE",               
            create_network_paths="DESTINATIONS_TO_SOURCES"
        )
        
        # Clean up temporary data
        arcpy.AddMessage("Cleaning up temporary files...")
        arcpy.management.Delete(r"memory\campus_route_back_direction")
        
        arcpy.AddMessage("Done.")
        
    except arcpy.ExecuteError:
        arcpy.AddError("ArcGIS tool error occurred:")
        arcpy.AddError(arcpy.GetMessages(2))
        raise
        
    except Exception as e:
        arcpy.AddError(f"Unexpected error occurred: {str(e)}")
        raise
    
def main():    
    pointOfBeginning = arcpy.GetParameterAsText(0)
    pointOfEnding = arcpy.GetParameterAsText(1)
    costRaster = arcpy.GetParameterAsText(2)
    
    find_campus_route(pointOfBeginning, pointOfEnding, costRaster)
    
    arcpy.SetParameterAsText(3, CAMPUS_ROUTE)
if __name__ == "__main__":
    main()
