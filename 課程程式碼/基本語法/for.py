index = 0
string = "Hello"

print("---第一個for迴圈，印出元素於同一行---")
for letter in string:
    index += 1
    if index==len(string):
        print(letter)
    else:
        print(letter, end='')

print("---第二個for迴圈，一行印出一個元素---")
for number in range(3):
    print(number)