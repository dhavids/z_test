class Answer:
    def __get__(self, obj, objtype):
        return 42
    def __set__(self, obj, value):
        obj.answer = value
class Universe:
    answer = Answer()

u = Universe()
print(u.answer) 

u.answer = 24

