class DutyRepo:
    def __init__(self):
        self.duties = []

    def add(self, duty):
        self.duties.append(duty)

    def get_all(self):
        return self.duties[:]