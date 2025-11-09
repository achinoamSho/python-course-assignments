import tkinter as tk
from tkinter import messagebox

def recommend_water_intake(weight_kg, age, activity_level):
    base_ml = weight_kg * 35
    if age < 18:
        base_ml *= 1.1
    elif age > 55:
        base_ml *= 0.9

    if activity_level == "low":
        base_ml *= 1.0
    elif activity_level == "medium":
        base_ml *= 1.2
    elif activity_level == "high":
        base_ml *= 1.4

    return base_ml / 1000

def calculate():
    try:
        weight = float(weight_entry.get())
        age = int(age_entry.get())
        activity = activity_var.get()

        liters = recommend_water_intake(weight, age, activity)
        result_label.config(text=f"Recommended: {liters:.2f} liters/day 💧")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

root = tk.Tk()
root.title("Water Intake Recommender")

tk.Label(root, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Age:").grid(row=1, column=0, padx=10, pady=5)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Activity level:").grid(row=2, column=0, padx=10, pady=5)
activity_var = tk.StringVar(value="medium")
tk.OptionMenu(root, activity_var, "low", "medium", "high").grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Calculate", command=calculate).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
