class Answer:
    def __get__(self, obj, objtype):
        return 42
    def __set__(self, obj, value):
        obj.answer = value
class Universe:
    answer = Answer()
    
u = Universe()
print(u.answer) # 42
# The following line will cause an error:
u.answer = 24 # maximum recursion depth exceeded