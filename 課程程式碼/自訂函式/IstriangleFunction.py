def isTriangle(side1, side2, side3):
    if not (side1 + side2 > side3):
        return False
    elif not (side1 + side3 > side2):
        return False
    else:
        return True

print(isTriangle(7,5,10))
print(isTriangle(2,8,1))