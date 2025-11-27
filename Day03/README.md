# Cell Culture Volume Calculator - Day03

This project calculates how much volume to take from a source plate of cultured cells to reach a desired confluency in a destination plate. It includes both a **GUI** and a **CLI** interface.

## Features
- Input source and destination plate types (or custom plates)
- Input current and desired confluency (%)
- Calculates volume to take from the source plate (GUI also shows how much fresh media to add)
- Error handling for impossible volumes or invalid inputs
- Tested calculation logic with `pytest`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/achinoamSho/python-course-assignments.git
cd python-course-assignments/Day03
```
2. Install dependencies:
```bash
pip install pytest click
```

**Dependencies used**:
- `pytest` (for testing)
- `click` (for improved CLI argument handling and automatic help generation)
- `tkinter` (built-in for GUI)

## Running the Program

**GUI**:
```bash
python cell_volume_gui.py
```

**CLI**:
```bash
python cell_volume_cli.py <current_conf> <current_area> <desired_conf> <dest_area> <current_vol>
```

To see detailed help with all argument descriptions, use the `--help` flag:
```bash
python cell_volume_cli.py --help
```

### CLI Arguments

The CLI requires 5 arguments (all numeric values):

1. **`current_conf`** (float): Current confluency (%) of the source plate  
   - Example: `50` (for 50% confluency)
   - Must be greater than 0
   - Represents the percentage of the plate surface covered by cells

2. **`current_area`** (float): Surface area (cm²) of the source plate  
   - Example: `60` (for a 10 cm plate)
   - Must be greater than 0
   - Common plate sizes:
     - 96-well: 0.33 cm²
     - 24-well: 2 cm²
     - 12-well: 4 cm²
     - 6-well: 10 cm²
     - 10 cm dish: 60 cm²

3. **`desired_conf`** (float): Target confluency (%) for the destination plate  
   - Example: `25` (for 25% confluency)
   - Must be greater than 0
   - The percentage of confluency you want to achieve in the destination plate

4. **`dest_area`** (float): Surface area (cm²) of the destination plate  
   - Example: `10` (for a 6-well plate)
   - Must be greater than 0
   - Same common values as `current_area` (see above)

5. **`current_vol`** (float): Total volume (µL) in the source plate after trypsinization  
   - Example: `3000` (for 3000 µL)
   - Must be greater than 0
   - The total volume of cell suspension in the source plate

### CLI Examples

Basic example (10 cm plate to 6-well plate):
```bash
python cell_volume_cli.py 50 60 25 10 3000
```
This calculates the volume to take from a 10 cm plate (60 cm²) with 50% confluency to achieve 25% confluency in a 6-well plate (10 cm²), assuming 3000 µL total volume in the source plate.

Example with smaller plates (96-well to 24-well):
```bash
python cell_volume_cli.py 80 0.33 40 2 200
```
This calculates the volume needed when transferring from a 96-well plate at 80% confluency to a 24-well plate at 40% confluency.

## Running Tests
pytest

## AI Usage

I used AI to:
- Refactor code and separate calculation logic into `calc_logic.py`
- Improve error checking and input validation
- Write and refine pytest test cases

Prompts included:
- "Refactor my cell volume calculation into a separate module and add error handling"
- "Write pytest tests for my calculation function with edge cases"
