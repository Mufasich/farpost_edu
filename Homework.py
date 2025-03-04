from datetime import datetime, timedelta


class Homework:

    def __init__(self, text: str, deadline: int):
        self.text = text
        self.deadline = timedelta(days=deadline)
        self.created = datetime.now()

    def is_active(self) -> bool:
        return datetime.now() - self.created < self.deadline