print("---先執行index+=1---")
index = 0
while index<3:
    index += 1
    print(str(index) + " x 10 = " + str(index*10))

print("---後執行index+=1---")
index = 0
while index<3:
    print(str(index) + " x 10 = " + str(index*10))
    index += 1