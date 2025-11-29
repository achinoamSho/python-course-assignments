# Copilot Instructions for Python Course Assignments

This repository contains Python course assignments organized by day. When assisting with code in this project, please follow these guidelines:

## Project Structure

- Assignments are organized by day (Day01, Day02, Day03, etc.)
- Each day typically includes:
  - Implementation files (`.py`)
  - README.md with project description and AI usage notes
  - Tests (when applicable, using `pytest`)

## Code Style & Best Practices

### General Python Guidelines
- Follow PEP 8 style guidelines
- Use descriptive variable names that reflect their purpose
- Include docstrings for functions and classes
- Keep functions focused on a single responsibility

### Error Handling
- Raise appropriate exceptions (e.g., `ValueError` for invalid inputs)
- Provide clear, helpful error messages
- Test error cases in test files

### Code Organization
- Separate business logic from UI code (e.g., `calc_logic.py` separate from `cell_volume_gui.py`)
- Keep calculation functions pure and testable
- Use modules to organize related functionality

## Testing

- Write tests using `pytest` for calculation logic and core functions
- Include both normal cases and edge cases (zero values, negative values, etc.)
- Test error conditions using `pytest.raises()`
- Keep test files named with `test_` prefix (e.g., `test_calc_logic.py`)

## GUI Development (Tkinter)

- Use `tkinter` for GUI applications
- Validate inputs before processing
- Provide user-friendly error messages
- Consider using dropdown menus for common values (e.g., plate sizes)
- Keep GUI code separate from calculation logic

## CLI Development

- Use `click` library for improved CLI argument handling
- Provide helpful `--help` documentation
- Include clear descriptions for all arguments
- Validate inputs and provide meaningful error messages

## Documentation

- Update README.md files with:
  - Project description and purpose
  - Installation instructions
  - Usage examples
  - Dependencies used
  - Notes on AI assistance (what was used and how)

## AI Assistance Guidelines

When helping with code:
- Suggest improvements that teach best practices
- Encourage separation of concerns (logic vs. UI)
- Help write tests to ensure code correctness
- Guide toward learning Python concepts, not just completing assignments

## Common Patterns in This Project

- **Cell culture calculations**: Mathematical formulas for laboratory work
- **Multiple interfaces**: CLI, interactive, and GUI versions of the same functionality
- **Input validation**: Always check for zero, negative, or invalid values
- **Modular design**: Separate calculation logic from user interface code

## Dependencies

Common dependencies used in this project:
- `pytest` - for testing
- `click` - for CLI argument handling
- `tkinter` - for GUI (built-in with Python)

When suggesting new dependencies, consider if they're necessary and appropriate for a learning context.

