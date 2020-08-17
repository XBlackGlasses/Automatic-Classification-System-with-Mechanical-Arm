# import Human package 以及 Calculator Module
import Human
import Calculator

# Human需產生實例，第一個Human為package，第二個Human為class
human1 = Human.Human('Jone', 179, 72)
human2 = Human.Human('Rose', 165, 48)

human1.say_my_name()
human2.say_my_name()
Calculator.print_the_module_name()

human1.name = 'Tom'
Calculator.module_name = "計算機"

print('-------After change-------')
human1.say_my_name()
human2.say_my_name()
Calculator.print_the_module_name()