from Teacher import Teacher
from Homework import Homework
from Student import Student



teacher = Teacher('Anton', 'Petrov')
student = Student('Kirill', 'Ivanov')


print(teacher.last_name)  # Daniil
print(student.first_name)  # Petrov

expired_homework = teacher.create_homework('Learn functions', 0)
print(expired_homework.created)  
print(expired_homework.deadline)  
print(expired_homework.text) 


create_homework_too = teacher.create_homework
oop_homework = create_homework_too('create 2 simple classes', 5)
oop_homework.deadline  # 5 days, 0:00:00

student.do_homework(oop_homework)
student.do_homework(expired_homework)  # You are late
