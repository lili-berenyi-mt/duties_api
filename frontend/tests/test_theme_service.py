from frontend.services import ThemeService
import pytest 

@pytest.fixture
def mock_repo(mocker):
    return mocker.Mock()

@pytest.fixture
def theme_service(mock_repo):
    return ThemeService(mock_repo)

def test_theme_service_toggles_status(mock_repo, theme_service):
    mock_repo.update_status.return_value = True

    result = theme_service.toggle_completion(theme_id="1", current_status=False)

    assert result is True
    mock_repo.update_status.assert_called_once_with("1", True)