from Homework import Homework

class Student:

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def do_homework(self, homework: Homework):
        if homework.is_active():
            return homework
        print('You are late')
        return None