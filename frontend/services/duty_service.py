from models import Duty
from .results import AddDutyResult

class DutyService:
    def __init__(self, repo):
        self.repo = repo

    def add(self, number, description):
        try:
            new_duty = Duty(number, description)
        except ValueError:
            return AddDutyResult.EMPTY_DESCRIPTION
        
        duties = self.repo.get_all()
        if any(duty.equals(new_duty) for duty in duties):
            return AddDutyResult.DUPLICATE
        self.repo.add(Duty(number, description))
        return AddDutyResult.SUCCESS
    
    def get_all(self):
        return self.repo.get_all()