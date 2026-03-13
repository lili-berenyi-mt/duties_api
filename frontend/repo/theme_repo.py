import requests
import os

class ThemeRepo:
    def __init__(self):
        self.api_url = os.getenv("BACKEND_URL", "http://localhost:5000")

    def update_status(self, theme_id, completed_status):
        try:
            response = requests.put(
                f"{self.api_url}/themes/{theme_id}",
                json={"completed": completed_status}
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False    