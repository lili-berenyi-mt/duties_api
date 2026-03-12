import pytest
from frontend.models import Duty

def test_duty_can_display_name():
    duty = Duty("D1", "Test 1")
    assert duty.get_code() == "D1"

    duty = Duty("D2", "Test 2")
    assert duty.get_code() == "D2"

def test_duty_can_return_summary():
    duty1 = Duty("D1", "Test description 1")
    assert duty1.get_summary() == "D1: Test description 1"

    duty2 = Duty("D2", "Test description 2")
    assert duty2.get_summary() == "D2: Test description 2"
    
def test_two_duties_are_equal():
    duty1a = Duty("D1", "Test description A")
    duty1b = Duty("D1", "Test description B")
    assert duty1a.equals(duty1b)
    assert duty1b.equals(duty1a)

def test_different_duties_are_not_equal():
    duty1 = Duty("D1", "Test")
    duty2 = Duty("D2", "Test")
    assert duty1.equals(duty2) == False

def test_cannot_create_duty_with_empty_description():
    with pytest.raises(ValueError):
        Duty("D1", "")

