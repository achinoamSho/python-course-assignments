import sys

from cell_volume_calc import calculate_volume

def safe_float(s):
    try:
        return float(s)
    except ValueError:
        return None

def main():
    if len(sys.argv) != 6:
        print("Usage: python cell_volume_cli.py <current_conf> <current_area> <desired_conf> <desired_area> <final_vol>")
        sys.exit(1)

    args = [safe_float(arg) for arg in sys.argv[1:]]
    if None in args:
        print("Error: all arguments must be numeric.")
        sys.exit(1)

    current_conf, current_area, desired_conf, desired_area, final_vol = args

    if current_conf <= 0 or current_area <= 0 or desired_conf <= 0 or desired_area <= 0 or final_vol <= 0:
        print("Error: all values must be positive numbers.")
        sys.exit(1)

    v_take = calculate_volume(current_conf, current_area, desired_conf, desired_area, final_vol)

    if v_take > final_vol:
        print(f"❌ Warning: required volume ({v_take:.2f} µL) exceeds available volume ({final_vol:.2f} µL).")
    else:
        print(f"✅ You should take {v_take:.2f} µL from the current plate.")

if __name__ == "__main__":
    main()
