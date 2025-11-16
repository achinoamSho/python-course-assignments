# Cell Culture Volume Calculator - Day03

This project calculates how much volume to take from a source plate of cultured cells to reach a desired confluency in a destination plate. It includes both a **GUI** and a **CLI** interface.

## Features
- Input source and destination plate types (or custom plates)
- Input current and desired confluency (%)
- Calculates volume to take and amount of fresh media to add
- Error handling for impossible volumes or invalid inputs
- Tested calculation logic with `pytest`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/achinoamSho/python-course-assignments.git
cd Day03
```
2. Install dependencies directly:
```bash
pip install pytest
```

**Dependencies used**:
- `pytest` (for testing)
- `tkinter` (built-in for GUI)
- No additional 3rd-party library was found for the calculation logic.

## Running the Program

**GUI**:
```bash
python cell_volume_gui.py
```

**CLI**:
```bash
python cell_volume_cli.py <current_conf> <current_area> <desired_conf> <desired_area> <final_vol>
```

## Running Tests
pytest

## AI Usage

I used AI to:
- Refactor code and separate calculation logic into `calc_logic.py`
- Add error handling and edge case checks
- Write test cases for the calculation logic

Prompts included:
- "Refactor my cell volume calculation into a separate module and add error handling"
- "Write pytest tests for my calculation function with edge cases"
