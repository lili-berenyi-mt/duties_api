class Duty:
    def __init__(self, number, description):
        if not description:
            raise ValueError("Description cannot be empty")
        self.number = number
        self.description = description

    def get_name(self):
        return f"Duty {self.number}"
    
    def get_summary(self):
        return f"{self.get_name()}: {self.description}"
    
    def equals(self, other):
        return self.number == other.number