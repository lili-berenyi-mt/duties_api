from frontend.models import Duty
from frontend.services.results import AddDutyResult

class DutyService:
    def __init__(self, repo):
        self.repo = repo

    def add(self, number, description):
        try:
            new_duty = Duty(number, description)
        except ValueError:
            return AddDutyResult.EMPTY_DESCRIPTION
        
        response = self.repo.add(new_duty)
        if response == "SUCCESS":
            return AddDutyResult.SUCCESS
        elif response == "DUPLICATE":
            return AddDutyResult.DUPLICATE
        elif response == "CONNECTION_FAILURE":
            return AddDutyResult.ERROR 
        return AddDutyResult.ERROR
    
    def get_all(self):
        return self.repo.get_all()