# Amino Acid Classification Quiz

This is a simple terminal-based quiz game for practicing basic amino acid properties.
The game randomly shows you amino acids and asks you to classify them by:

- **charge** - `positive` / `negative` / `neutral`
- **polarity** - `polar` / `nonpolar`
- **aromaticity** - `aromatic` / `non-aromatic`

You choose which category you want to practice and how many questions to answer.

## Files

- `amino_acids_game.py` - main game code (can be run directly).
- `test_game.py` - tests for the core logic. to run the test:
```bash
pytest
```

## Requirements

- **Python 3.10+**  
- No external libraries are required to play the game.
- (Optional) [`pytest`](https://pytest.org/) if you want to run the tests.

To install `pytest`:

```bash
pip install pytest
```

## How to play:

After running the game, type `1`, `2`, or `3` to choose a category.

Enter how many questions you want (e.g. `5` or `10`).

For each amino acid, type your answer (e.g. `polar`, `non-aromatic`, `positive`).

At the end, your score will be displayed.

To quit at category selection, type `q`.

Good luck!

<img src="https://github.com/user-attachments/assets/a2c4619f-ade2-431c-99bf-58ecf90b8961" alt="Amino Acids" width="800">


