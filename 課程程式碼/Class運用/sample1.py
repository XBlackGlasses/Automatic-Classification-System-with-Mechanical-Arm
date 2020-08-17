# .py檔屬於class的管理作用，所以需寫成以下型式，
# 可理解成從HumanClass.py檔中載入Human的class
from HumanClass import Human
# 亦或者單純import HumanClass，
# 並在human錢加上HumanClass.，如以下註解部分



# human1 = HumanClass.Human('Rose', 168, 50)
human1 = Human('Rose', 168, 50)
human1.say_my_name()
print('My BMI is ' + str(human1.getBMI()))

# human2 = HumanClass.Human('jone', 180, 73)
human2 = Human('jone', 180, 73)
human2.say_my_name()
print('My BMI is ' + str(human2.getBMI()))