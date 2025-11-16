from calc_logic import calculate_volume
import pytest

# Normal calculation
def test_basic():
    vol = calculate_volume(50, 10, 25, 10, 2000)
    assert vol == 1000

# Errors for invalid inputs
def test_error_zero_desired():
    with pytest.raises(ValueError):
        calculate_volume(50, 10, 0, 10, 2000)

def test_error_zero_current_conf():
    with pytest.raises(ValueError):
        calculate_volume(0, 10, 25, 10, 2000)

def test_error_zero_current_area():
    with pytest.raises(ValueError):
        calculate_volume(50, 0, 25, 10, 2000)

def test_error_zero_dest_area():
    with pytest.raises(ValueError):
        calculate_volume(50, 10, 25, 0, 2000)
