from frontend.services import ThemeService, ToggleThemeResult
import pytest 

@pytest.fixture
def mock_repo(mocker):
    return mocker.Mock()

@pytest.fixture
def theme_service(mock_repo):
    return ThemeService(mock_repo)

def test_authenticated_user_can_toggle_theme(mock_repo, theme_service):
    mock_repo.update_status.return_value = True
    result = theme_service.toggle_completion(theme_id="1", user_role="user", current_status=False)
    assert result == True
    mock_repo.update_status.assert_called_once_with("1", True)

def test_unauthenticated_user_cannot_toggle_theme(mock_repo, theme_service):
    mock_repo.update_status.return_value = True
    result = theme_service.toggle_completion(theme_id="1", current_status=False, user_role=None)
    assert result == ToggleThemeResult.UNAUTHORISED
    mock_repo.save.assert_not_called()