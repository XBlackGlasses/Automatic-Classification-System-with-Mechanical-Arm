# import Human package 以及 Calculator Module
import Human
import Calculator

# Human需產生實例，第一個Human為package，第二個Human為class
human1 = Human.Human('Jone', 179, 72)
human1.say_my_name()

#Calculator 裡的function直接使用即可
sum = Calculator.add_two_num(27, 593)
print(sum)
Calculator.print_the_module_name()