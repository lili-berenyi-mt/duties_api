from services import DutyService, AddDutyResult
from models import Duty

def test_duty_can_be_added(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get_all.return_value = []
    duty_service = DutyService(mock_repo)

    result = duty_service.add(number=1, description="test")

    mock_repo.add.assert_called_once()
    assert result == AddDutyResult.SUCCESS

def test_can_add_multiple_duties(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get_all.return_value = []
    duty_service = DutyService(mock_repo)

    result1 = duty_service.add(1, "Test1")
    result2 = duty_service.add(2, "Test2")

    assert result1 == AddDutyResult.SUCCESS
    assert result2 == AddDutyResult.SUCCESS
    assert mock_repo.add.call_count == 2

def test_duplicate_duty_cannot_be_added(mocker):
    mock_repo = mocker.Mock()
    existing_duty = Duty(1, "Test")
    mock_repo.get_all.return_value = {existing_duty}
    duty_service = DutyService(mock_repo)

    duty_service.add(number=1, description="test1")
    result = duty_service.add(number=1, description="test2")

    assert mock_repo.add.call_count == 0
    assert result == AddDutyResult.DUPLICATE

def test_duty_with_empty_description_cannot_be_added(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get_all.return_value = []
    duty_service = DutyService(mock_repo)

    result = duty_service.add(1,"")

    assert mock_repo.add.call_count == 0
    assert result == AddDutyResult.EMPTY_DESCRIPTION
    

def test_can_read_all_duties(mocker):
    mock_repo = mocker.Mock()
    duty1 = Duty(1, "Test")
    duty2 = Duty(2, "Test")
    duty3 = Duty(3, "Test")
    mock_repo.get_all.return_value = [duty1, duty2, duty3]
    duty_service = DutyService(mock_repo)

    result = duty_service.get_all()

    assert result == [duty1, duty2, duty3]

def test_returns_empty_list_when_no_duties(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get_all.return_value = []
    duty_service = DutyService(mock_repo)

    result = duty_service.get_all()

    assert result == []