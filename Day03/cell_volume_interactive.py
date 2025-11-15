# cell_volume_input.py
from cell_volume_calc import calculate_volume

def safe_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive numeric value.")

def main():
    current_conf = safe_float_input("Current confluency (%): ")
    current_area = safe_float_input("Current plate surface area (cm²): ")
    desired_conf = safe_float_input("Desired confluency (%): ")
    desired_area = safe_float_input("Desired plate surface area (cm²): ")
    final_vol = safe_float_input("Final volume on new plate (µL): ")

    v_take = calculate_volume(current_conf, current_area, desired_conf, desired_area, final_vol)

    if v_take > final_vol:
        print(f"❌ Warning: required volume ({v_take:.2f} µL) exceeds available volume ({final_vol:.2f} µL).")
    else:
        print(f"✅ You should take {v_take:.2f} µL from the current plate.")

if __name__ == "__main__":
    main()
