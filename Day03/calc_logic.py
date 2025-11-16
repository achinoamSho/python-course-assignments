def calculate_volume(current_conf, current_area, desired_conf, dest_area, current_volume):
    """
    Calculate how much volume should be transferred based on confluency and area.
    Returns the volume (µL) to take from the current plate.
    """

    # Validate inputs
    if current_conf <= 0:
        raise ValueError("Current confluency must be > 0")
    if desired_conf <= 0:
        raise ValueError("Desired confluency must be > 0")
    if current_area <= 0 or dest_area <= 0:
        raise ValueError("Plate areas must be > 0")
    if current_volume <= 0:
        raise ValueError("Current volume must be > 0")

    # Compute required transfer volume
    cells_now = current_conf * current_area
    cells_needed = desired_conf * dest_area

    fraction_needed = cells_needed / cells_now
    return current_volume * fraction_needed
