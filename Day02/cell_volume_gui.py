import tkinter as tk
from tkinter import ttk, messagebox

# Plate info: area (cm²) and final culture volume (µL)
plates = {
    "96 well (0.33 cm², 100 µL)": {"area": 0.33, "final_vol": 100},
    "24 well (2 cm², 500 µL)": {"area": 2, "final_vol": 500},
    "12 well (4 cm², 1000 µL)": {"area": 4, "final_vol": 1000},
    "6 well (10 cm², 2000 µL)": {"area": 10, "final_vol": 2000},
    "10 cm (60 cm², 10000 µL)": {"area": 60, "final_vol": 10000}
}

# ---------- Helper functions ----------

def safe_float(s):
    try:
        return float(s)
    except ValueError:
        return None

def on_current_plate_change(event=None):
    """Prefill nothing, just placeholder."""
    current_vol_entry.delete(0, tk.END)

def reset_fields():
    current_plate_dropdown.current(4)   # 10 cm
    destination_plate_dropdown.current(3)  # 6 well
    current_conf_entry.delete(0, tk.END)
    desired_conf_entry.delete(0, tk.END)
    current_vol_entry.delete(0, tk.END)
    result_label.config(text="", foreground="black")

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

        current_area = plates[current_plate_key]["area"]
        dest_area = plates[destination_plate_key]["area"]
        dest_final_vol = plates[destination_plate_key]["final_vol"]

        # Calculation logic
        x = (current_conf * current_area) / (desired_conf * dest_area)
        volume_to_take = current_vol / x
        media_to_add = dest_final_vol - volume_to_take

        # Build result text
        text_lines = []
        color = "green"

        if volume_to_take > current_vol:
            text_lines.append(
                f"❌ Not enough volume in the current plate!\n"
                f"   Needed: {volume_to_take:.1f} µL\n"
                f"   Available: {current_vol:.1f} µL\n"
                f"   ➤ Try reducing desired confluency or splitting into multiple plates.\n"
            )
            color = "red"
        elif volume_to_take > dest_final_vol:
            text_lines.append(
                f"⚠️ Volume exceeds the final volume of the destination plate!\n"
                f"   Volume to take: {volume_to_take:.1f} µL\n"
                f"   Destination final volume: {dest_final_vol:.1f} µL\n"
                f"   ➤ You’ll need multiple wells or a larger plate.\n"
            )
            color = "red"
        else:
            text_lines.append(f"✅ Take {volume_to_take:.1f} µL from the current plate.")
            text_lines.append(f"Add {media_to_add:.1f} µL of fresh media to reach a total of {dest_final_vol:.0f} µL.")

        # Display result
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

# Current plate inputs
ttk.Label(frame, text="Current plate type:").grid(row=0, column=0, sticky="w", pady=5)
current_plate_var = tk.StringVar(value=list(plates.keys())[4])
current_plate_dropdown = ttk.Combobox(frame, textvariable=current_plate_var, values=list(plates.keys()), width=40, state="readonly")
current_plate_dropdown.grid(row=0, column=1, pady=5)
current_plate_dropdown.bind("<<ComboboxSelected>>", on_current_plate_change)

ttk.Label(frame, text="Current confluency (%):").grid(row=1, column=0, sticky="w", pady=5)
current_conf_entry = ttk.Entry(frame, width=10)
current_conf_entry.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Total volume after trypsinization (µL):").grid(row=2, column=0, sticky="w", pady=5)
current_vol_entry = ttk.Entry(frame, width=10)
current_vol_entry.grid(row=2, column=1, pady=5)

# Destination plate inputs
ttk.Label(frame, text="Destination plate type:").grid(row=3, column=0, sticky="w", pady=5)
destination_plate_var = tk.StringVar(value=list(plates.keys())[3])
destination_plate_dropdown = ttk.Combobox(frame, textvariable=destination_plate_var, values=list(plates.keys()), width=40, state="readonly")
destination_plate_dropdown.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Desired confluency (%):").grid(row=4, column=0, sticky="w", pady=5)
desired_conf_entry = ttk.Entry(frame, width=10)
desired_conf_entry.grid(row=4, column=1, pady=5)

# Buttons
btn_frame = ttk.Frame(frame)
btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
ttk.Button(btn_frame, text="Calculate", command=calculate).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="Reset", command=reset_fields).grid(row=0, column=1, padx=8)

# Result display
result_label = ttk.Label(frame, text="", wraplength=560, justify="left", font=("Arial", 11))
result_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=10)

root.mainloop()
