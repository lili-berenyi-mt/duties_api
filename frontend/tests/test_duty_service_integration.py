import pytest
import requests
from frontend.repo import DutyRepo
from frontend.services import DutyService, AddDutyResult
from frontend.models import Duty

@pytest.fixture
def mock_post(mocker):
    return mocker.patch('requests.post')

@pytest.fixture
def duty_service():
    repo = DutyRepo()
    return DutyService(repo)

def test_integration_api_conflict_returns_duplicate(duty_service, mock_post):
    mock_post.return_value.status_code = 409
    result = duty_service.add(1, "test")
    assert result == AddDutyResult.DUPLICATE

def test_integration_api_down_returns_error(duty_service, mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError()
    result = duty_service.add(1, "test")
    assert result == AddDutyResult.ERROR