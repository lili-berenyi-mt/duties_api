import requests
import os
from frontend.models import Duty

class DutyRepo:
    def __init__(self):
        self.api_url = os.getenv("BACKEND_URL", "http://localhost:5000")
        self.duties = []

    def add(self, duty):
        try:
            payload = {
                "code": duty.code, 
                "description": duty.description
            }
            response = requests.post(f"{self.api_url}/duties", json=payload)

            if response.status_code == 201:
                return "SUCCESS"
            if response.status_code == 409:
                return "DUPLICATE"
            if response.status_code == 400:
                return "INVALID"
            return "ERROR"

        except requests.exceptions.RequestException:
            return "CONNECTION_FAILURE"

    def get_all(self):
        try:
            response = requests.get(f"{self.api_url}/duties")
            data = response.json()
            return [Duty(item['code'], item['description']) for item in data]
        except Exception as e:
            print(f"API Error: {e}")
            return []
        
    def get_by_code(self, code):
        try:
            response = requests.get(f"{self.api_url}/duties/search/{code}")
            if response.status_code == 200:
                data = response.json()
                duty = Duty(data['duty'], data["description"])
                duty.themes = data.get('themes', []) 
                return duty
            return None
        except requests.exceptions.RequestException as e:
            print(f"Database/API Connection Error: {e}")
            return None
    