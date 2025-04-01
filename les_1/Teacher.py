from Homework import Homework

class Teacher:

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def create_homework(text: str, deadline: int) -> Homework:
        return Homework(text, deadline)
