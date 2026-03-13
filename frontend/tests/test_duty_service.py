from frontend.services import DutyService, AddDutyResult
from frontend.models import Duty
import pytest

@pytest.fixture
def mock_repo(mocker):
    return mocker.Mock()

@pytest.fixture
def duty_service(mock_repo):
    return DutyService(mock_repo)

def test_duty_can_be_added(mock_repo, duty_service):
    mock_repo.get_all.return_value = []
    mock_repo.add.return_value = "SUCCESS"
    result = duty_service.add(number=1, description="test")

    mock_repo.add.assert_called_once()
    assert result == AddDutyResult.SUCCESS

def test_can_add_multiple_duties(mock_repo, duty_service):
    mock_repo.get_all.return_value = []
    mock_repo.add.return_value = "SUCCESS"

    result1 = duty_service.add(1, "Test1")
    result2 = duty_service.add(2, "Test2")

    assert result1 == AddDutyResult.SUCCESS
    assert result2 == AddDutyResult.SUCCESS
    assert mock_repo.add.call_count == 2

def test_duplicate_duty_cannot_be_added(mock_repo, duty_service):
    mock_repo.add.return_value = "DUPLICATE"
    result = duty_service.add(number=1, description="test2")

    assert mock_repo.add.call_count == 1
    assert result == AddDutyResult.DUPLICATE

def test_duty_with_empty_description_cannot_be_added(mock_repo, duty_service):
    mock_repo.get_all.return_value = []

    result = duty_service.add(1,"")

    assert mock_repo.add.call_count == 0
    assert result == AddDutyResult.EMPTY_DESCRIPTION
    

def test_can_read_all_duties(mock_repo, duty_service):
    duty1 = Duty(1, "Test")
    duty2 = Duty(2, "Test")
    duty3 = Duty(3, "Test")
    mock_repo.get_all.return_value = [duty1, duty2, duty3]

    result = duty_service.get_all()

    assert result == [duty1, duty2, duty3]

def test_returns_empty_list_when_no_duties(mock_repo, duty_service):
    mock_repo.get_all.return_value = []

    result = duty_service.get_all()

    assert result == []

def test_get_by_code_returns_duty_with_coins(duty_service, mock_repo):
    duty = Duty("D5", "Test Description")
    duty.themes = ["Example1", "Example2"]
    mock_repo.get_by_code.return_value = duty

    result = duty_service.get_by_code("D5")

    assert result.code == "D5"
    assert "Example1" in result.themes
    assert len(result.themes) == 2

def test_cannot_add_duty_with_non_numeric_number(duty_service, mock_repo):
    result = duty_service.add(number="one", description="test1")
    assert result == AddDutyResult.INVALID_INPUT

def test_delete_returns_false_if_not_found(duty_service, mock_repo):
    mock_repo.delete_by_code.return_value = False
    result = duty_service.delete_by_code("D404")
    assert result is False
    mock_repo.delete_by_code.assert_called_once_with("D404")

def test_delete_returns_true_if_found_and_deleted(duty_service, mock_repo):
    mock_repo.delete_by_code.return_value = True
    result = duty_service.delete_by_code("D1")
    assert result is True
    mock_repo.delete_by_code.assert_called_once_with("D1")