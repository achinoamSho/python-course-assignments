def calculate_volume(current_conf, current_area, desired_conf, dest_area, current_volume):
    """
    Calculate how much volume should be transferred based on confluency and area.
    Returns the volume (µL) to take from the current plate.
    """
    if current_conf <= 0 or current_area <= 0:
        raise ValueError("Current confluency and area must be greater than 0")

    cells_now = current_conf * current_area
    cells_needed = desired_conf * dest_area

    fraction_needed = cells_needed / cells_now
    return current_volume * fraction_needed
