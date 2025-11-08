# cell_volume_input.py
from cell_volume_calc import calculate_volume

current_conf = float(input("Current confluency (%): "))
current_area = float(input("Current plate surface area (cm²): "))
desired_conf = float(input("Desired confluency (%): "))
desired_area = float(input("Desired plate surface area (cm²): "))
final_vol = float(input("Final volume on new plate (µL): "))

v_take = calculate_volume(current_conf, current_area, desired_conf, desired_area, final_vol)
print(f"You should take {v_take:.2f} µL from the current plate.")
