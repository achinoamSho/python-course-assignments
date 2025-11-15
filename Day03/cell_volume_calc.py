"""
    Calculate the volume to take from a current plate of cultured cells to reach desired confluency in a new plate.
    
    Parameters:
        current_conf: current confluency (%) of source plate
        current_area: surface area (cm²) of source plate
        desired_conf: desired confluency (%) on new plate
        desired_area: surface area (cm²) of new plate
        final_vol: final total volume (µL) in current plate after trypsinization
    
    Returns:
        float: Volume to take from current plate (µL)

"""
def calculate_volume(current_conf, current_area, desired_conf, desired_area, final_vol):
    return final_vol*((desired_conf * desired_area) /(current_conf * current_area))

  
