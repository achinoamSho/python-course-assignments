"""
Simple GUI for the One Piece Card Game downloader.

Uses tkinter (built into Python) as the UI.
Business logic lives in optcg_logic.py.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, scrolledtext

from optcg_logic import (
    get_card_data,
    save_card_json,
    download_card_images,
)


def format_card_summary(card_data) -> str:
    """Return a text summary for a single card version."""
    name = card_data.get("card_name", "Unknown name")
    set_name = card_data.get("set_name", "Unknown set")
    rarity = card_data.get("rarity", "Unknown rarity")
    card_type = card_data.get("card_type", "Unknown type")
    color = card_data.get("card_color", "Unknown color")
    power = card_data.get("card_power", "N/A")
    life = card_data.get("life", "N/A")
    market_price = card_data.get("market_price", "N/A")
    inv_price = card_data.get("inventory_price", "N/A")
    text = card_data.get("card_text", "")

    lines = [
        f"Name       : {name}",
        f"Set        : {set_name}",
        f"Rarity     : {rarity}",
        f"Type/Color : {card_type} / {color}",
        f"Power      : {power}   |   Life: {life}",
        f"Prices     : inventory={inv_price} USD, market={market_price} USD",
        "",
        "Effect text:",
        text or "(no effect text)",
        "-" * 60,
    ]
    return "\n".join(lines)


class OnePieceGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("One Piece Card Downloader (Day 04)")

        # --- Top frame: input + button ---
        top_frame = tk.Frame(root)
        top_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(top_frame, text="Card ID (e.g. OP01-001):").pack(side="left")

        self.card_id_var = tk.StringVar()
        self.entry = tk.Entry(top_frame, textvariable=self.card_id_var, width=20)
        self.entry.pack(side="left", padx=5)

        self.fetch_button = tk.Button(top_frame, text="Fetch card", command=self.on_fetch)
        self.fetch_button.pack(side="left", padx=5)

        # --- Middle: checkbox for images ---
        options_frame = tk.Frame(root)
        options_frame.pack(padx=10, pady=(0, 5), fill="x")

        self.download_images_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options_frame,
            text="Download images",
            variable=self.download_images_var,
        ).pack(side="left")

        # --- Text area to show results ---
        self.text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.text.pack(padx=10, pady=10, fill="both", expand=True)

        # Focus the entry on start
        self.entry.focus_set()

    def on_fetch(self) -> None:
        card_id = self.card_id_var.get().strip()
        if not card_id:
            messagebox.showwarning("Missing input", "Please enter a card ID, e.g. OP01-001.")
            return

        # Clear previous text
        self.text.delete("1.0", tk.END)

        # Fetch card data using business logic
        try:
            data = get_card_data(card_id)
        except Exception as err:
            messagebox.showerror("Error", f"Could not fetch data for {card_id}:\n{err}")
            return

        if not data:
            messagebox.showinfo("No data", f"No data returned for card ID {card_id}.")
            return

        # Show summary for each version
        self.text.insert(tk.END, f"Found {len(data)} version(s) for card ID {card_id}:\n\n")
        for idx, card in enumerate(data, start=1):
            self.text.insert(tk.END, f"Version {idx}:\n")
            self.text.insert(tk.END, format_card_summary(card))
            self.text.insert(tk.END, "\n\n")

        # Save JSON
        try:
            json_path = save_card_json(card_id, data)
        except Exception as err:
            messagebox.showerror("Error", f"Could not save JSON:\n{err}")
            return

        self.text.insert(tk.END, f"Saved full JSON data to: {json_path}\n")

        # Optionally download images
        if self.download_images_var.get():
            try:
                paths = download_card_images(data)
            except Exception as err:
                messagebox.showerror("Error", f"Could not download images:\n{err}")
                return

            if paths:
                self.text.insert(tk.END, "\nSaved image files:\n")
                for p in paths:
                    self.text.insert(tk.END, f"  {p}\n")
            else:
                self.text.insert(tk.END, "\nNo image URLs found in the data.\n")


def main() -> None:
    root = tk.Tk()
    app = OnePieceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
