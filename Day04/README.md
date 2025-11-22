# One Piece Card Downloader

For the Day04 assignment I built a small Python program that downloads data about **One Piece Trading Card Game** cards using the public **OPTCG API** (One Piece Card Game API).
My husband collects One Piece cards as a hobby so I thought creating a program that will provide the data easily.

The program has a **graphical user interface (GUI)** where the user can:
- Enter a card ID (e.g. `OP01-001`)
- Fetch information about all versions of that card (normal, parallel, etc.)
- See a summary (name, set, rarity, type, color, power, life, prices, effect text)
- Save the full card data to a local JSON file
- Optionally download the real card images to disk

---

## Data source

The data is downloaded from the public **OPTCG API** for the One Piece Card Game:

- Base URL: `https://optcgapi.com/api`
- Example endpoint used in the code: `https://optcgapi.com/api/sets/card/OP01-001/`

This API returns JSON with card details, including image URLs, which my program then uses to save the data locally.

---

## Files in this folder

- `optcg_logic.py`  
  Business logic module. Contains functions that:
  - Call the OPTCG API and return parsed JSON data:
    - `get_card_data(card_id: str) -> list[dict]`
  - Save card data as pretty-printed JSON:
    - `save_card_json(card_id, data, output_dir="onepiece_cards")`
  - Download card images from the API’s image URLs:
    - `download_card_images(data, output_dir="onepiece_cards/images")`
  This module **does not** do any user interaction (no `input()` or `print()`).

- `optcg_gui.py`  
  GUI (User Interface) built with `tkinter` that:
  - Displays a window with:
    - Text field for the card ID
    - Checkbox “Download images”
    - “Fetch card” button
    - Scrollable text area for the results
  - Uses the functions from `optcg_logic.py` to:
    - Fetch card data
    - Save JSON
    - Optionally download images
  All user interaction (inputs, buttons, pop-ups) is here.

---

## Separation of business logic and UI

The assignment asked to separate “business logic” from the UI. In this project:

- **Business logic** = `optcg_logic.py`  
  - Talks to the API  
  - Parses JSON  
  - Saves files  
  - Can be reused by any interface (GUI, CLI, tests)

- **UI (User Interface)** = `optcg_gui.py`  
  - Handles user inputs (card ID, “download images” checkbox)  
  - Shows messages and card summaries in a window  
  - Calls the functions from `optcg_logic.py` to actually do the work  

This makes it easy to change the interface later (e.g. add a command-line version) without touching the logic.

---

## Installation / Requirements

I did use `uv` on my computer. Instead I installed the dependencies with `pip`.

Requirements:

- Python 3.x
- `requests` (for HTTP)
- `tkinter` (comes with the standard Python installation on Windows)

To install the Python packages (from any terminal):

```bash
python -m pip install requests pytest
```
##  AI

I used ChatGPT (OpenAI, GPT-5.1) to help with this assignment. The AI helped me:

- Design the separation between business logic (`optcg_logic.py`) and the graphical user interface (`optcg_gui.py`).
- Write and refine the initial versions of these two files.
- Understand how relative paths and `.gitignore` work for keeping downloaded data (JSON + images) out of the git repository.

I reviewed and adapted the generated code and text to match my local setup (using `pip` instead of `uv`) and the course requirements.
