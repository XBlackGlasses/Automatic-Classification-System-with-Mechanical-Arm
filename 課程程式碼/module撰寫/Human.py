class Human:
    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight
    
    def say_my_name(self):
        print('My name is ' + self.name + '.')
        