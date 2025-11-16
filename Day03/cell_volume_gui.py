import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from calc_logic import calculate_volume

# Plate info: area (cm²) and final culture volume (µL)
plates = {
    "96 well (0.33 cm², 100 µL)": {"area": 0.33, "final_vol": 100},
    "24 well (2 cm², 500 µL)": {"area": 2, "final_vol": 500},
    "12 well (4 cm², 1000 µL)": {"area": 4, "final_vol": 1000},
    "6 well (10 cm², 2000 µL)": {"area": 10, "final_vol": 2000},
    "10 cm (60 cm², 10000 µL)": {"area": 60, "final_vol": 10000},
    "Other": {"area": None, "final_vol": None}
}

# ---------- Helper functions ----------

def safe_float(s):
    try:
        return float(s)
    except ValueError:
        return None

def reset_fields():
    current_plate_dropdown.current(4) 
    destination_plate_dropdown.current(3)  # 6 well
    current_conf_entry.delete(0, tk.END)
    desired_conf_entry.delete(0, tk.END)
    current_vol_entry.delete(0, tk.END)
    result_label.config(text="", foreground="black")

def get_plate_params(key):
    """Return area and final_vol. If Other, ask user for input."""
    if key != "Other":
        return plates[key]["area"], plates[key]["final_vol"]
    else:
        area = simpledialog.askfloat("Custom plate", "Enter plate area (cm²):", minvalue=0.01)
        final_vol = simpledialog.askfloat("Custom plate", "Enter final volume (µL):", minvalue=1)
        return area, final_vol

# ---------- Main calculation ----------

def calculate():
    try:
        current_plate_key = current_plate_var.get()
        destination_plate_key = destination_plate_var.get()
        current_conf = safe_float(current_conf_entry.get())
        desired_conf = safe_float(desired_conf_entry.get())
        current_vol = safe_float(current_vol_entry.get())

        if not all([current_conf, desired_conf, current_vol]):
            messagebox.showerror("Input error", "Please enter numeric values for all fields.")
            return

        if current_conf <= 0 or desired_conf <= 0:
            messagebox.showerror("Input error", "Confluency values must be > 0.")
            return

        current_area, _ = get_plate_params(current_plate_key)
        dest_area, dest_final_vol = get_plate_params(destination_plate_key)

        volume_to_take = calculate_volume(current_conf, current_area, desired_conf, dest_area, current_vol)
        media_to_add = dest_final_vol - volume_to_take

        # Build result text
        text_lines = []
        color = "green"

        if volume_to_take > current_vol:
            text_lines.append(
                f"❌ Not enough volume in the current plate!\n"
                f"   Needed: {volume_to_take:.1f} µL\n"
                f"   Available: {current_vol:.1f} µL"
            )
            color = "red"
        elif volume_to_take > dest_final_vol:
            text_lines.append(
                f"⚠️ Volume exceeds destination plate final volume!\n"
                f"   Volume to take: {volume_to_take:.1f} µL\n"
                f"   Destination final volume: {dest_final_vol:.1f} µL"
            )
            color = "red"
        else:
            text_lines.append(f"✅ Take {volume_to_take:.1f} µL from the current plate.")
            text_lines.append(f"Add {media_to_add:.1f} µL of fresh media to reach a total of {dest_final_vol:.0f} µL.")

        result_label.config(text="\n".join(text_lines), foreground=color)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong.\n\n{e}")

# ---------- GUI setup ----------

root = tk.Tk()
root.title("🧫 Cell Culture Transfer Calculator")
root.geometry("600x420")
root.resizable(False, False)

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Current plate type:").grid(row=0, column=0, sticky="w", pady=5)
current_plate_var = tk.StringVar(value=list(plates.keys())[4])
current_plate_dropdown = ttk.Combobox(frame, textvariable=current_plate_var, values=list(plates.keys()), width=40, state="readonly")
current_plate_dropdown.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Current confluency (%):").grid(row=1, column=0, sticky="w", pady=5)
current_conf_entry = ttk.Entry(frame, width=10)
current_conf_entry.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Total volume after trypsinization (µL):").grid(row=2, column=0, sticky="w", pady=5)
current_vol_entry = ttk.Entry(frame, width=10)
current_vol_entry.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Destination plate type:").grid(row=3, column=0, sticky="w", pady=5)
destination_plate_var = tk.StringVar(value=list(plates.keys())[3])
destination_plate_dropdown = ttk.Combobox(frame, textvariable=destination_plate_var, values=list(plates.keys()), width=40, state="readonly")
destination_plate_dropdown.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Desired confluency (%):").grid(row=4, column=0, sticky="w", pady=5)
desired_conf_entry = ttk.Entry(frame, width=10)
desired_conf_entry.grid(row=4, column=1, pady=5)

btn_frame = ttk.Frame(frame)
btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
ttk.Button(btn_frame, text="Calculate", command=calculate).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="Reset", command=reset_fields).grid(row=0, column=1, padx=8)

result_label = ttk.Label(frame, text="", wraplength=560, justify="left", font=("Arial", 11))
result_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=10)

root.mainloop()
