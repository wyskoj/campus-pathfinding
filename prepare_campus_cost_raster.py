"""
Campus Cost Raster Generator
============================
This script creates a cost raster for campus routing by converting walkway polygons
to a raster and reclassifying indoor/outdoor areas with appropriate cost values.
The resulting cost raster can be used for optimal path analysis that prioritizes
indoor routes over outdoor paths.
Author: Jacob Wysko
Date: November 2025
"""
import arcpy
def create_campus_cost_raster(walkways, environmentField, indoorFieldValue, outdoorFieldValue, 
                            indoorCostValue, outdoorCostValue, cellsize, costRaster):
    """
    Creates a cost raster for campus routing analysis.
    
    This function converts walkway polygons to a raster and reclassifies the values
    to create a cost surface where indoor pathways have lower cost values than outdoor
    paths. This encourages routing algorithms to prefer indoor routes when available.
    
    Args:
        walkways (str): Path to walkway polygon feature layer
        environmentField (str): Field name containing environment classification
        indoorFieldValue (str): Value representing indoor areas in classification field
        outdoorFieldValue (str): Value representing outdoor areas in classification field
        indoorCostValue (str): Cost value to assign to indoor areas (typically lower)
        outdoorCostValue (str): Cost value to assign to outdoor areas (typically higher)
        cellsize (str): Cell size for output raster
        costRaster (str): Output path for cost raster
        
    Returns:
        None: Output is saved to specified cost raster location
    """
    
    try:
        # Step 1: Convert walkway polygons to raster
        arcpy.AddMessage("Converting walkway polygons to raster...")
        arcpy.conversion.PolygonToRaster(
            in_features=walkways,
            value_field=environmentField,
            out_rasterdataset=r"memory\WalkwaysRaster",
            cell_assignment="CELL_CENTER",
            priority_field="NONE",
            cellsize=cellsize,
            build_rat="BUILD"
        )
        
        # Step 2: Reclassify raster values to cost values
        arcpy.AddMessage("Reclassifying indoor and outdoor cost values...")
        out_raster = arcpy.sa.Reclassify(
            in_raster=r"memory\WalkwaysRaster",
            reclass_field=environmentField,
            remap=f"{outdoorFieldValue} {outdoorCostValue};{indoorFieldValue} {indoorCostValue}",
            missing_values="DATA"
        )
        
        arcpy.AddMessage(f"Saving cost raster to: {costRaster}")
        out_raster.save(costRaster)
        
        arcpy.AddMessage("Cleaning up temporary files...")
        arcpy.management.Delete(r"memory\WalkwaysRaster")
        
        arcpy.AddMessage("Done.")
        
    except arcpy.ExecuteError:
        arcpy.AddError("ArcGIS tool error occurred:")
        arcpy.AddError(arcpy.GetMessages(2))
        raise
        
    except Exception as e:
        arcpy.AddError(f"Unexpected error occurred: {str(e)}")
        raise
    
def main():    
    walkways = arcpy.GetParameterAsText(0)
    environmentField = arcpy.GetParameterAsText(1)
    indoorFieldValue = arcpy.GetParameterAsText(2)
    outdoorFieldValue = arcpy.GetParameterAsText(3)
    indoorCostValue = arcpy.GetParameterAsText(4)
    outdoorCostValue = arcpy.GetParameterAsText(5)
    cellsize = arcpy.GetParameterAsText(6)
    costRaster = arcpy.GetParameterAsText(7) 
    
    create_campus_cost_raster(walkways, environmentField, indoorFieldValue, outdoorFieldValue,
                            indoorCostValue, outdoorCostValue, cellsize, costRaster)
if __name__ == "__main__":
    main()
