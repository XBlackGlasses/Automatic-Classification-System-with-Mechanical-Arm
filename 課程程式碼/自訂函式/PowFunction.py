def myPow(num1, num2):
    output = 1
    while (num2 > 0):
        output = output * num1
        num2 = num2 - 1
    return output

print(myPow(2,2))
print(myPow(3,2))
print(myPow(10,3))