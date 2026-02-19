from repo import DutyRepo
from services import DutyService, AddDutyResult

def test_add_duty():
    duty_repo = DutyRepo()
    duty_service = DutyService(duty_repo)

    result = duty_service.add(1, "test")
    assert result == AddDutyResult.SUCCESS

    duties = duty_service.get_all()
    assert len(duties) == 1
    assert duties[0].get_name() == "Duty 1"
    assert duties[0].get_summary() == "Duty 1: test"

def test_add_and_read_multiple_duties():
    duty_repo = DutyRepo()
    duty_service = DutyService(duty_repo)

    result1 = duty_service.add(1, "Test A")
    result2 = duty_service.add(2, "Test B")
    result2 = duty_service.add(3, "Test C")

    duties = duty_service.get_all()
    assert len(duties) == 3

    names = [duty.get_name() for duty in duties]
    assert names == ["Duty 1", "Duty 2", "Duty 3"]


def test_cannot_add_duplicate_duty():
    duty_repo = DutyRepo()
    duty_service = DutyService(duty_repo)

    duty_service.add(1, "test A")
    result = duty_service.add(1, "test B")
    duties = duty_service.get_all()

    assert result == AddDutyResult.DUPLICATE
    assert len(duties) == 1
    assert duties[0].get_summary() == "Duty 1: test A"


def test_cannot_add_duty_with_empty_description():
    duty_repo = DutyRepo()
    duty_service = DutyService(duty_repo)

    result = duty_service.add(1, "")
    duties = duty_service.get_all()

    assert result == AddDutyResult.EMPTY_DESCRIPTION
    assert len(duties) == 0

def test_returns_empty_list_when_no_duties():
    duty_repo = DutyRepo()
    duty_service = DutyService(duty_repo)
    
    duties = duty_service.get_all()

    assert duties == []