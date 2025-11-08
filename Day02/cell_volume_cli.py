import sys

from cell_volume_calc import calculate_volume

if len(sys.argv) != 6:
    print("Usage: python cell_volume_cli.py <current_conf> <current_area> <desired_conf> <desired_area> <final_vol>")
    sys.exit()

args = [float(arg) for arg in sys.argv[1:]]
v_take = calculate_volume(*args)
print(f"You should take {v_take:.2f} µL from the current plate.")
