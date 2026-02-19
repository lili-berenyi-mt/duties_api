import pytest
from models import Duty

def test_duty_can_display_name():
    duty = Duty(1, "Test 1")
    assert duty.get_name() == "Duty 1"

    duty = Duty(2, "Test 2")
    assert duty.get_name() == "Duty 2"

def test_duty_can_return_summary():
    duty1 = Duty(1, "Test description 1")
    assert duty1.get_summary() == "Duty 1: Test description 1"

    duty2 = Duty(2, "Test description 2")
    assert duty2.get_summary() == "Duty 2: Test description 2"
    
def test_two_duties_are_equal():
    duty1a = Duty(1, "Test description A")
    duty1b = Duty(1, "Test description B")
    assert duty1a.equals(duty1b)
    assert duty1b.equals(duty1a)

def test_different_duties_are_not_equal():
    duty1 = Duty(1, "Test")
    duty2 = Duty(2, "Test")
    assert duty1.equals(duty2) == False

def test_cannot_create_duty_with_empty_description():
    with pytest.raises(ValueError):
        Duty(1, "")

