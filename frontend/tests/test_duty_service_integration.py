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

def test_repo_get_by_code_maps_themes(mocker):
    mock_get = mocker.patch('requests.get')
    mock_response = mocker.Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "duty": "D1",
        "description": "Test 1",
        "themes": [
            {"id": "1", "name": "Theme1", "completed": False}
        ]
    }
    mock_get.return_value = mock_response

    repo = DutyRepo()

    result = repo.get_by_code("D1")

    assert result.code == "D1"
    assert result.themes[0]["name"] == "Theme1"
    assert result.themes[0]["id"] == "1"
    assert "/duties/search/D1" in mock_get.call_args[0][0]