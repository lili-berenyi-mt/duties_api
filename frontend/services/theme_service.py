class ThemeService:
    def __init__(self, repo):
        self.repo = repo

    def toggle_completion(self, theme_id, current_status):
        new_status = not current_status
        return self.repo.update_status(theme_id, new_status)