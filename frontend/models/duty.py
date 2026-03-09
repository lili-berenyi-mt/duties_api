class Duty:
    def __init__(self, code, description):
        if not description:
            raise ValueError("Description cannot be empty")
        self.code = code
        self.description = description

    def get_code(self):
        return self.code
    
    def get_summary(self):
        return f"{self.get_code()}: {self.description}"
    
    def equals(self, other):
        return self.code == other.code