from frontend.services.results import ToggleThemeResult
class ThemeService:
    def __init__(self, repo):
        self.repo = repo

    def toggle_completion(self, theme_id, current_status, user_role):
        if user_role == None:
            return ToggleThemeResult.UNAUTHORISED
        new_status = not current_status
        return self.repo.update_status(theme_id, new_status)